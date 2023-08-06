from dsopz.config import config
from dsopz import io
from dsopz import util
import json as JSON
from dsopz.processor import blockify, dispatch
from dsopz.datastore import mutation
import logging as log

class Error(Exception):
    """Exceptions"""

def resolve_query(dataset, namespace, gql=None, query=None, kind=None, plain=None, gz=None):
    query = [JSON.loads(q) if isinstance(q, str) else q for q in (query or [])]
    if kind:
        query = [{'kind': [{'name': k}]} for k in kind]
    if gql or query:
        ret = gql or query
        return { 'dataset': dataset, 'namespace': namespace, 'queries': ret }
    if plain or gz:
        with io.jreader(plain, gz) as f:
            header = next(f)
            queries = header['queries']
            for line in f:
                queryidx = line['queryIndex']
                cursor = line['cursor']
                queries[queryidx]['startCursor'] = cursor
            return header
    raise Error('error')

def resolve_mutation_skip(resume):
    if not resume:
        return 0
    try:
        with io.jreader(resume) as r:
            ret = None
            for l in r:
                ret = l
            return ret['processed']
    except FileNotFoundError:
        return 0

class Mutation(object):

    def __init__(self, dataset, namespace, file, file_gz, resume):
         self._dataset = dataset
         self._namespace = namespace
         self._file = file
         self._file_gz = file_gz
         self._resume_file = resume

    def _resume(self):
        start = None
        block = []
        with io.jreader(self._file, self._file_gz) as f:
            f = enumerate(f)
            for i in range(self._skip):
                log.info('Skipping: %s', i)
                next(f)
            for idx, line in f:
                if start == None:
                    start = idx
                line = self._parse_line(line)
                if line:
                    block.append(line)
                if len(block) >= 500:
                    yield (start, idx, block)
                    block = []
                    start = None
            if len(block) > 0:
                yield (start, idx, block)

    def _consume_buffer(self, limit):
        while len(self._buffer) > limit:
            p_start, p_end, p_block, p_fut = self._buffer.pop(0)
            log.info('Waiting for: [%s - %s], len: %s', p_start, p_end, len(p_block))
            p_fut.result()
            if self._resume_file:
                io.write_all(self._resume_file, append=True, lines=[{'processed':p_end+1}])

    def execute(self):
        self._skip = resolve_mutation_skip(self._resume_file)
        log.info('Skip: %s', self._skip)
        self._buffer = []
        for start, end, block in self._resume():
            log.info('Processing: [%s - %s], len: %s', start, end, len(block))
            self._consume_buffer(19)
            upserts, removes = self._operation(block)
            fut = dispatch(mutation, self._dataset, self._namespace, upserts=upserts, removes=removes)
            self._buffer.append( (start, end, block, fut) )
        self._consume_buffer(0)
        log.info('Done')

class UpsertMutation(Mutation):

    def _parse_line(self, line):
        return line.get('entity')

    def _operation(self, block):
        return (block, None)


class RemoveMutation(Mutation):

    def _parse_line(self, line):
        return line.get('entity', {}).get('key')

    def _operation(self, block):
        return (None, block)
