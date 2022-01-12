"""
Implements AFEP.

## Assumptions:
* Each file *.txt downloaded from Wikipedia, etc., must have the
    source name (e.g., Wikipedia_COVID.txt).
* If there are multiple files, ensure that all of the text for the same source
    share the same content before the first underscore. E.g., if text from Mayo Clinic was split up, try:
    * Mayo_COVID-19_0.txt
    * Mayo_COVID-19_1.txt
    * Mayo_COVID-19_2.txt
    * Mayo_COVID-19_3.txt
"""
import datetime
import math
import pathlib
import json
import pandas as pd
from loguru import logger
import click

from pyphenorm.afep.semtypes import SEMTYPES


@click.command()
@click.argument('datadirs', nargs=-1, type=click.Path(exists=True, path_type=pathlib.Path, file_okay=False), )
@click.option('--outformat', default='json',
              help='Metamaplite output format.')
@click.option('--outpath', default=None, type=click.Path(exists=True, path_type=pathlib.Path, file_okay=False),
              help='Directory to place output.')
def run_afep_selection(datadirs: list[pathlib.Path], *, outformat='json', outpath: pathlib.Path = None):
    """
    Run afep on the output directory from Metamaplite. AFEP will select a minimum set of CUIs
        to supply to PheNorm for feature selection. For more details, see the PheNorm paper.

    :param datadirs: data directories with output json files from running Metamaplite
    :param outformat: only json is currently supported
    :param outpath: output directory (default is current directory)
    :return:
    """
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    if not outpath:
        outpath = pathlib.Path('.')
    # extract CUIs from supported filetype/output format from metamaplite
    df = pd.DataFrame.from_records(extract_from_directories(datadirs, outformat=outformat))

    # retain only those CUIs with at least half the sources
    df = include_cuis_in_half_of_sources(df)

    # use greedy algorithm to eliminate duplicates
    chosen_cuis = greedy_eliminate_cuis(df)

    # create final dictionary
    res_dict_df = df[df['cui'].isin(chosen_cuis)].groupby(['cui', 'preferredname']).agg({
        'conceptstring': lambda x: ','.join(set(x)),
        'matchedtext': lambda x: ','.join(set(x)),
        'all_sources': lambda x: ','.join(set(x)),
        'all_semantictypes': lambda x: ','.join(set(x)),
    }).reset_index()

    # output dictionary and text file of found cuis
    outpath.mkdir(exist_ok=True)
    res_dict_df.to_csv(outpath / f'afep_dict_{now}.csv', index=False)
    with open(outpath / f'afep_selected_cuis_{now}.csv', 'w') as out:
        out.write('\n'.join(res_dict_df['cui'].unique()))


def greedy_eliminate_cuis(df: pd.DataFrame):
    # cui -> number of source dictionaries with this cui; for tie-breaking
    cui_to_source_count = {r.cui: len(r.all_sources.split(',')) for r in
                           df[['cui', 'all_sources']].drop_duplicates().itertuples()}
    # don't use length: assume any starting position has the same text
    cui_df = df.query('>0 or '.join(SEMTYPES) + '>0')[
        ['cui', 'matchedtext', 'docid', 'start', 'length']
    ].groupby(
        ['docid', 'start', 'matchedtext', 'cui']
    ).count().reset_index()
    cui_as_col_df = cui_df.pivot(index=['docid', 'matchedtext', 'start'], columns='cui',
                                 values='length').fillna(0).reset_index()

    # run greedy algorithm
    n_cui_starting = cui_df['cui'].nunique()
    res = greedy_algorithm(cui_as_col_df.copy(), cui_to_source_count)
    n_cui_ending = len(res)
    logger.info(f'Completed: greedy algorithm reduced {n_cui_starting} to {n_cui_ending}.')
    return res


def greedy_algorithm(temp_df, cui_to_source_count):
    res = []
    while temp_df.shape[0] > 0:
        _temp_df = temp_df[[col for col in temp_df.columns if str(col).startswith('C')]].sum()
        max_val = _temp_df.max()
        cuis = list(_temp_df[_temp_df == max_val].index)
        d = {c: cui_to_source_count[c] for c in cuis}
        cui = max(d, key=d.get)
        res.append(cui)
        logger.debug(f'Adding cui {cui} which covers {max_val} `matchedtext`s.')
        temp_df = temp_df[temp_df[cui] == 0.0]
    return res


def include_cuis_in_half_of_sources(df: pd.DataFrame):
    total_sources = df['article_type'].nunique()
    half_sources = int(math.ceil(total_sources / 2))
    logger.info(f'Only retain CUIs appearing in >= {half_sources} sources.')
    before_cui_count = df['cui'].nunique()
    s = df[['cui', 'article_type']].drop_duplicates().groupby('cui').count()
    cuis_with_at_least_half = set(s[s.article_type >= half_sources].index)
    logger.info(f'Reduced CUIs from {before_cui_count} to {len(cuis_with_at_least_half)}.')
    return df[df.cui.isin(cuis_with_at_least_half)]


def extract_from_directories(datadirs: list[pathlib.Path], *, outformat='json'):
    for outdir in datadirs:
        for file in outdir.glob('*.json'):
            if outformat == 'json':
                article_type = file.stem.split('_')[0]
                with open(file) as fh:
                    data = json.load(fh)
                for i, row in enumerate(extract_mml_from_json(data)):
                    row['event_id'] = f'{file.stem}_{i}'
                    row['article_type'] = article_type
                    row['docid'] = file.stem
                    yield row
            else:
                raise ValueError(f'Outputformat `{outformat}` not implemented.')


def extract_mml_from_json(data):
    for el in data:
        for event in el['evlist']:
            yield {
                      'matchedtext': event['matchedtext'],
                      'conceptstring': event['conceptinfo']['conceptstring'],
                      'cui': event['conceptinfo']['cui'],
                      'preferredname': event['conceptinfo']['preferredname'],
                      'start': event['start'],
                      'length': event['length'],
                      'evid': event['id'],
                      'negated': el.get('negated', None),
                      'first_semantictype': event['conceptinfo']['semantictypes'][0],
                      'first_source': event['conceptinfo']['sources'][0],
                      'all_sources': ','.join(event['conceptinfo']['sources']),
                      'all_semantictypes': ','.join(event['conceptinfo']['semantictypes']),
                  } | {
                      s: 1 for s in event['conceptinfo']['sources']
                  } | {
                      s: 1 for s in event['conceptinfo']['semantictypes']
                  }


if __name__ == '__main__':
    run_afep_selection()
