""" test script agent in pycoq 
"""
import asyncio
import os

from typing import Iterable

import pycoq.opam
import pycoq.common
import pycoq.agent


import epycoq, coq


async def tutorial_deterministic_agent(theorems: Iterable):
    """
    a snipped of code demonstrating usage of pycoq
    """

    # create default coq context for evaluation of a theorem
    coq_ctxt = pycoq.common.CoqContext(pwd=os.getcwd(),
                                       executable='',
                                       target='serapi_shell')
    cfg = pycoq.opam.opam_serapi_cfg(coq_ctxt)

    newtip = 2
    ontop = 1

    print(coq_ctxt)

    # create python coq-serapi object that wraps API of the coq-serapi  
    async with pycoq.serapi.CoqSerapi(cfg) as ucoq:
        for prop, script in theorems:

            # execute proposition of the theorem
            # print(">> exec with u-pycoq <<")
            # _, _, coq_exc, _ = await ucoq.execute(prop)
            # if coq_exc:
            #     print(f"{prop} raised coq exception {coq_exc}")
            #     continue

            # or try with e-pycoq
            print(">> exec with e-pycoq <<")
            opts = {"newtip": newtip, "ontop": ontop, "lim": 10 }
            res = coq.add(prop, opts)
            print('res', res)
            res = coq.exec(newtip)
            print('res', res)
            newtip += 1
            ontop += 1

            # execute the proof script of the theorem
            print(">> exec proof with e-pycoq <<")
            opts = {"newtip": newtip, "ontop": ontop, "lim": 10 }
            res = coq.add('Proof.', opts)
            print('res', res)
            newtip += 1
            ontop += 1
            opts = {"newtip": newtip, "ontop": ontop, "lim": 10 }
            res = coq.add('auto.', opts)
            print('res', res)
            newtip += 1
            ontop += 1
            opts = {"newtip": newtip, "ontop": ontop, "lim": 10 }
            res = coq.add('Qed.', opts)
            print('res', res)
            newtip += 1
            ontop += 1

            print(">> print ast with e-pycoq <<")
            ppopts = { "pp_format": ("PpSer",None), "pp_depth": 1000, "pp_elide": "...", "pp_margin": 90}
            opts = {"limit": 100, "preds": [], "sid": 5, "pp": ppopts, "route": 0}
            cmd = ('Ast',None)
            res = coq.query(opts, cmd)
            print(res)
            
            print("==========================================")


            # n_steps, n_goals = await pycoq.agent.script_agent(ucoq, script)

            # msg = f"Proof {script} fail" if n_goals != 0 else f"Proof {script} success"
            # print(f"{prop} ### {msg} in {n_steps} steps\n")


def main():

    theorems = [
        ("Theorem th4: forall A B C D: Prop, A->(A->B)->(B->C)->(C->D)->D.",
         ["auto."]),
        ("Theorem th5: forall A B C D E: Prop, A->(A->B)->(B->C)->(C->D)->E.",
         ["auto."]),
        ("Theorem th6: forall A B C D E: Prop, A->(A->B)->(B->C)->(C->D)->(D->E)->E.",
         ["auto."])]
        

    asyncio.run(tutorial_deterministic_agent(theorems))

if __name__ == '__main__':
    main()
    
    


            
