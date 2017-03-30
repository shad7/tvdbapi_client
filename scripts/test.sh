#!/bin/bash


run_test() {
    pip install --quiet -e .
    nosetests --exe
}

run_cover() {
    pip install --quiet -e .
    COVERAGE_FILE=.coverage."${PY_VERSION}" nosetests --exe --with-coverage --cover-package="${PROJECT}"
}

run_merge() {
    coverage combine
    coverage html -d cover
}

case "$1" in
    --merge)
        run_merge ;;
    --cover)
        run_cover ;;
    *)
        run_test ;;
esac
