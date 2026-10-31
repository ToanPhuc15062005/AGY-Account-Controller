$env:PYTHONPATH = "$PSScriptRoot\src;$env:PYTHONPATH"
python -m agy_mas.cli.main $args
