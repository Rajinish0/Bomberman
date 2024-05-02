# SCRIPT FOR RUNNING TESTS ON WINDOWS

$env:PYTHONPATH='./'
py -m unittest discover -s tests -p "test_*.py"