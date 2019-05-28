from tables import undirected_resultslp, undirected_data, directed_data, nc_data, all_methods, all_datasets, resultsnc
from auto_docker import make_container, install_requirements, execute_train, execute_evaluation
from make_scripts import maketrainlp, maketrainnc, makeevallp, makeevalnc

make_container()
maketrainlp(['NetMF'], ['BlogCatalog'])
maketrainnc(['NetMF'], ['BlogCatalog'])
install_requirements('NetMF')
execute_train()
makeevallp(['NetMF'], ['BlogCatalog'])
makeevallp(['NetMF'], ['BlogCatalog'])

