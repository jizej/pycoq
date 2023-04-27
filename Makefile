.PHONY: help build install test clean

PYNAME=epycoq
SERAPI=coq-serapi/coq-serapi.install

help:
	@echo targets {build,install,test,clean}

# coq-serapi.install is required so plugins are in place [runtime dep]
build:
	dune build $(SERAPI) epycoq/$(PYNAME).so

install:
	dune build @pip-install

test:
	dune build @examples/runtest

clean:
	dune clean
