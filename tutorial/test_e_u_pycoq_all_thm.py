from typing import Union
import asyncio

import pycoq
from pycoq.common import CoqContext
from pycoq.opam import strace_build_coq_project_and_get_filenames
from pycoq.project_splits import get_proj_splits_based_on_name_of_path2data, CoqProjs
from pycoq.serapi import execute
from pycoq.utils import get_coq_serapi

# import epycoq, ucoq
import logging


async def example_execute_coq_files_from_coq_proj_in_pycoq(path2data: str = '~/data/lf_proj/'):
    coq_projs: CoqProjs = get_proj_splits_based_on_name_of_path2data(path2data)
    path2filenames_raw: list[str] = [strace_build_coq_project_and_get_filenames(coq_proj, make_clean_coq_proj=True) for coq_proj in coq_projs.coq_projs]
    path2filename: str
    print(coq_projs.coq_projs)
    print(path2filenames_raw)
    for path2filename in path2filenames_raw:
        coq_ctxt: CoqContext = pycoq.common.load_context(path2filename)
        cfg = pycoq.opam.opam_serapi_cfg(coq_ctxt)
        async with pycoq.serapi.CoqSerapi(cfg) as ucoq:
            stmts_in_file: iter[str] = pycoq.split.coq_stmts_of_context(coq_ctxt)
            for stmt_id, stmt in enumerate(stmts_in_file):
                print(stmt_id, stmt)

if __name__ == '__main__':
    import time
    import sys
    level    = logging.INFO
    handlers = [logging.FileHandler('./pycoq.log'), logging.StreamHandler()]
    

    logging.basicConfig(level = level, handlers=handlers)

    start_time = time.time()
    # - compile coq proj files in pycoq
    log = logging.getLogger(__name__)
    log.info("does this work???")
    # print(">> Parsing lf_coq_project <<")
    # asyncio.run(example_execute_coq_files_from_coq_proj_in_pycoq('lf_coq_project'))
    print("\n\n\n")
    print(">> Parsing coqgym <<")
    asyncio.run(example_execute_coq_files_from_coq_proj_in_pycoq('coqgym'))

    # - done
    duration = time.time() - start_time
    print(f"Done! {duration=}\n\a")
