
def maketrainlp(methods, datasets):
    f = open('/home/congttn/badne/code/lpexperiments/lptrain_methods.sh', "w+")
    f.write('''rootfolder="/data"
dir=$rootfolder'/data'
    cd $rootfolder'/code/methods/'

    for method in''')
    for i in range(len(methods)):
        f.write(" " + methods[i])
    
    f.write(''';
    do
        methodname=$method
        cd $rootfolder/code/methods/$methodname
        command=""
        for dataset in''')


    for i in range(len(datasets)):
        f.write(" " + datasets[i])
    
    f.write('''
        do
            f=$(ls $dir/$dataset/edgelist/LPSplit/*_train_0.[5,6])
            direction='directed'
            if [[ $f == *"BlogCatalog"* || $f == *"Flickr"*  || $f == *"Reddit"* || $f == *"PPI"* || $f == *"Youtube"* || $f == *"dblp-coauthor"* ]]; then
                echo "matched"
                direction='undirected'
            fi
            trainfile=$(echo $f | awk -F  "/" '{print $NF}')
            echo $trainfile

            cd $rootfolder/code/methods/$methodname
            ./train.sh $f $rootfolder/embeddings/LP/$methodname-$trainfile.embeddings $direction & done
    done''')
    f.close()

def maketrainnc(methods, datasets):
    f = open('/home/congttn/badne/code/ncexperiments/nctrain_methods.sh', "w+")
    f.write('''rootfolder="/data"
dir=$rootfolder'/data'
	cd $rootfolder'/code/methods/'
	
	for method in''')
    for i in range(len(methods)):
        f.write(" " + methods[i])
    
    f.write(''';
    do
		methodname=$method
		cd $rootfolder/code/methods/$methodname
		command=""
        for dataset in''')


    for i in range(len(datasets)):
        f.write(" " + datasets[i])
    
    f.write(''';
		do
			f=$dir/$dataset/edgelist/$dataset-edgelist.txt
			direction='directed'
			if [[ $f == *"BlogCatalog"* || $f == *"Flickr"*  || $f == *"Reddit"* || $f == *"PPI"* || $f == *"Youtube"* || $f == *"dblp-coauthor"* ]]; then
				echo "matched"
  				direction='undirected'
			fi
			
			trainfile=$(echo $f | awk -F  "/" '{print $NF}')
			cd $rootfolder/code/methods/$methodname && ./train.sh $f $rootfolder/embeddings/NC/$methodname-$trainfile.embeddings $direction & done
	done''')
    f.close()


def makeevallp(methods, datasets):
    f = open('/home/congttn/badne/code/evaluation/eval/evallp.sh', "w+")
    f.write('''rootfolder="/data"
dir=$rootfolder'/data'
	cd $rootfolder'/code/methods/'
	Count=0
	cores=24
	for method in''')

    for i in range(len(methods)):
        f.write(" " + methods[i])
    
    f.write(''';
	do
		methodname=$method
		cd $rootfolder/code/methods/$methodname
		for dataset in''')
    
    for i in range(len(datasets)):
        f.write(" " + datasets[i])
    
    f.write(''';
		do
			f=$(ls $dir/$dataset/edgelist/LPSplit/*_train_0.[5,6])
			directed=1
			if [[ $f == *"BlogCatalog"* || $f == *"Flickr"*  || $f == *"Reddit"* || $f == *"PPI"* || $f == *"Youtube"* || $f == *"dblp-coauthor"* ]]; then
  				directed=0
			fi

			trainfile=$(echo $f | awk -F  "/" '{print $NF}')
			embeddings=$rootfolder/embeddings/LP/$methodname-$trainfile.embeddings
			fullgraph=$rootfolder/data/$dataset/edgelist/$dataset-edgelist.txt
			evalscript=$rootfolder/code/evaluation/eval/link_pred.py
			resfile=$rootfolder/embeddings/LP/lp-results.txt
			frac='test_0.5'
			if [[ $f == *"Twitter"* ]]; then
				frac='test_0.6'
			fi
			testfile=$(echo ${rootfolder}/data/$dataset/edgelist/LPSplit/${dataset}_${frac})
			if [[ $methodname == *"SDNE"* ]]; then
				embeddings=$embeddings.mat
			fi
			if [[ $methodname == *"DNGR"* ]]; then
				embeddings=$embeddings.pkl
			fi

			additionalflags=""
			if [[ $directed -eq 1 ]];then
				if [[ $methodname == *"APP"* ]];then
					if [[ -f $embeddings-128.src ]];then
					echo python3 $evalscript $fullgraph $testfile $embeddings-128.tgt $embeddings-128.src -f 0  --random_seed 100 -directed 1 --result_file $resfile \&
					echo python3 $evalscript $fullgraph $testfile $embeddings-128.src $embeddings-128.src -f 0  --random_seed 100 -directed 1 --result_file $resfile \&
					Count=$(expr $Count + 2)
					if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
					 sleep 2  &
					echo python3 $evalscript $fullgraph $testfile $embeddings-128.tgt $embeddings-128.src -f 0.5  --random_seed 100 -directed 1 --result_file $resfile \&
					echo python3 $evalscript $fullgraph $testfile $embeddings-128.src $embeddings-128.src -f 0.5  --random_seed 100 -directed 1 --result_file $resfile \&
					Count=$(expr $Count + 2)
					if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
					 sleep 2  &
					echo python3 $evalscript $fullgraph $testfile $embeddings-128.tgt $embeddings-128.src -f 1  --random_seed 100 -directed 1 --result_file $resfile \&
					echo python3 $evalscript $fullgraph $testfile $embeddings-128.src $embeddings-128.src -f 1  --random_seed 100 -directed 1 --result_file $resfile \&
					Count=$(expr $Count + 2)
					if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
					 sleep 2  &
					fi
				
				elif [[ $methodname == *"node2vec"* ]];then
					for p in 0.25 0.5 1 2 4
					do
						for q in 0.25 0.5 1 2 4
						do
							node2vecembeddingfile=$embeddings-p$p-q$q.embeddings
							if [[ -f $node2vecembeddingfile ]]; then
							echo python3 $evalscript $fullgraph $testfile $node2vecembeddingfile $node2vecembeddingfile -f 0 --random_seed 100 -directed 1 --result_file $resfile \&
							Count=$(expr $Count + 1)
							if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
							 sleep 2  &
							echo python3 $evalscript $fullgraph $testfile $node2vecembeddingfile $node2vecembeddingfile -f 0.5 --random_seed 100 -directed 1 --result_file $resfile \&
							Count=$(expr $Count + 1)
							if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
							 sleep 2  &
							echo python3 $evalscript $fullgraph $testfile $node2vecembeddingfile $node2vecembeddingfile -f 1 --random_seed 100 -directed 1 --result_file $resfile \&
							Count=$(expr $Count + 1)
							if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
							 sleep 2  &
							fi
						done
					done
				
				elif [[ $methodname == *"LINE"* ]];then

					echo python3 $evalscript $fullgraph $testfile $embeddings-LINE-concatenated $embeddings-LINE-concatenated -f 0 --random_seed 100 $additionalflags  --result_file $resfile -directed 1 -b \&
					Count=$(expr $Count + 1)
					if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
					echo python3 $evalscript $fullgraph $testfile $embeddings-LINE1-normalized-128 $embeddings-LINE1-normalized-128 -f 0 --random_seed 100 $additionalflags  --result_file $resfile -directed 1 -b \&
					Count=$(expr $Count + 1)
					if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
					echo python3 $evalscript $fullgraph $testfile $embeddings-LINE2-normalized-128 $embeddings-LINE2-normalized-128 -f 0 --random_seed 100 $additionalflags  --result_file $resfile -directed 1 -b \&
					Count=$(expr $Count + 1)
					if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi

					echo python3 $evalscript $fullgraph $testfile $embeddings-LINE-concatenated $embeddings-LINE-concatenated -f 0.5 --random_seed 100 $additionalflags  --result_file $resfile -directed 1 -b \&
					Count=$(expr $Count + 1)
					if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
					echo python3 $evalscript $fullgraph $testfile $embeddings-LINE1-normalized-128 $embeddings-LINE1-normalized-128 -f 0.5 --random_seed 100 $additionalflags  --result_file $resfile -directed 1 -b \&
					Count=$(expr $Count + 1)
					if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
					echo python3 $evalscript $fullgraph $testfile $embeddings-LINE2-normalized-128 $embeddings-LINE2-normalized-128 -f 0.5 --random_seed 100 $additionalflags  --result_file $resfile -directed 1 -b \&
					Count=$(expr $Count + 1)
					if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi

					echo python3 $evalscript $fullgraph $testfile $embeddings-LINE-concatenated $embeddings-LINE-concatenated -f 1 --random_seed 100 $additionalflags  --result_file $resfile -directed 1 -b \&
					Count=$(expr $Count + 1)
					if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
					echo python3 $evalscript $fullgraph $testfile $embeddings-LINE1-normalized-128 $embeddings-LINE1-normalized-128 -f 1 --random_seed 100 $additionalflags  --result_file $resfile -directed 1 -b \&
					Count=$(expr $Count + 1)
					if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
					echo python3 $evalscript $fullgraph $testfile $embeddings-LINE2-normalized-128 $embeddings-LINE2-normalized-128 -f 1 --random_seed 100 $additionalflags  --result_file $resfile -directed 1 -b \&
					Count=$(expr $Count + 1)
					if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
					 
				else

						if [[ $methodname == *"NetMF"* ]]; then
						embeddings1=$embeddings-small.npy
						additionalflags="--npy"
						if [[ -f $embeddings1 ]]; then
						echo python3 $evalscript $fullgraph $testfile $embeddings1 $embeddings1 -f 0 --random_seed 100 $additionalflags -directed 1 --result_file $resfile \&
						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
						 sleep 2  &
						echo python3 $evalscript $fullgraph $testfile $embeddings1 $embeddings1 -f 0.5 --random_seed 100 $additionalflags -directed 1 --result_file $resfile \&
						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
						 sleep 2  &
						echo python3 $evalscript $fullgraph $testfile $embeddings1 $embeddings1 -f 1 --random_seed 100 $additionalflags -directed 1 --result_file $resfile \&
						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
						 sleep 2  &
						fi
						embeddings=$embeddings-large.npy
					fi
					if [[ $methodname == *"GraphSAGE"* ]]; then


						for model in graphsage_seq gcn graphsage_maxpool graphsage_meanpool graphsage_maxpool n2v graphsage_mean;do
							for lr in 0.0001 0.00001; do
								additionalflags=" --node_id_file $embeddings-$model-lr$lr.embeddingsval.txt"
						if [[ -f $embeddings"-$model-lr$lr.embeddingsval.npy" ]];then
						embeddingsfile=$embeddings"-$model-lr$lr.embeddingsval.npy"
						echo python3 $evalscript $fullgraph $testfile $embeddingsfile $embeddingsfile -f 0 --random_seed 100 $additionalflags  -directed 1 --result_file $resfile \&
						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
						echo python3 $evalscript $fullgraph $testfile $embeddingsfile $embeddingsfile -f 0.5 --random_seed 100 $additionalflags  -directed 1 --result_file $resfile \&
						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
						echo python3 $evalscript $fullgraph $testfile $embeddingsfile $embeddingsfile -f 1 --random_seed 100 $additionalflags  -directed 1 --result_file $resfile \&
						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
						 sleep 2  &
						fi
						done
						done

						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
					fi
				if [[ $methodname == *"verse"* ]];then
					additionalflags="--verse 128"
			 	fi
			 	if [[ -f $embeddings ]]; then
						echo python3 $evalscript $fullgraph $testfile $embeddings $embeddings -f 0 --random_seed 100 $additionalflags -directed 1 --result_file $resfile \&
						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
						 sleep 2  &
						echo python3 $evalscript $fullgraph $testfile $embeddings $embeddings -f 0.5 --random_seed 100 $additionalflags -directed 1 --result_file $resfile \&
						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
						 sleep 2  &
						echo python3 $evalscript $fullgraph $testfile $embeddings $embeddings -f 1 --random_seed 100 $additionalflags -directed 1 --result_file $resfile \&
						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
						 sleep 2  &
				fi
						 embeddings=""
				fi
						
			elif [[ $directed -eq 0 ]];then
					if [[ $methodname == *"APP"* ]];then
						if [[ -f $embeddings-128.src ]]; then

					echo python3 $evalscript $fullgraph $testfile $embeddings-128.tgt $embeddings-128.src -f 0 --random_seed 100 --result_file $resfile -directed 0 \&
					echo python3 $evalscript $fullgraph $testfile $embeddings-128.src $embeddings-128.src -f 0 --random_seed 100 --result_file $resfile -directed 0 \&
					Count=$(expr $Count + 2)
					if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
					 sleep 2  &
			fi
	
		
				elif [[ $methodname == *"node2vec"* ]];then
					for p in 0.25 0.5 1 2 4
					do
						for q in 0.25 0.5 1 2 4
						do
							node2vecembeddingfile=$embeddings-p$p-q$q.embeddings
							if [[ -f $node2vecembeddingfile ]]; then
							echo python3 $evalscript $fullgraph $testfile $node2vecembeddingfile $node2vecembeddingfile -f 0 --random_seed 100 --result_file $resfile -directed 0 \&
							Count=$(expr $Count + 1)
							if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
							 sleep 2  &
							fi
						done
					done
				elif [[ $methodname == *"LINE"* ]];then
					echo python3 $evalscript $fullgraph $testfile $embeddings-LINE-concatenated $embeddings-LINE-concatenated -f 0 --random_seed 100 $additionalflags  --result_file $resfile -directed 0 -b \&
					Count=$(expr $Count + 1)
					if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
					echo python3 $evalscript $fullgraph $testfile $embeddings-LINE1-normalized-128 $embeddings-LINE1-normalized-128 -f 0 --random_seed 100 $additionalflags  --result_file $resfile -directed 0 -b \&
					Count=$(expr $Count + 1)
					if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
					echo python3 $evalscript $fullgraph $testfile $embeddings-LINE2-normalized-128 $embeddings-LINE2-normalized-128 -f 0 --random_seed 100 $additionalflags  --result_file $resfile -directed 0 -b \&
					Count=$(expr $Count + 1)
					if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
					 sleep 2  &
				
					elif [[ $methodname == *"NetMF"* ]]; then

						if [[ -f $embeddings ]]; then
						echo python3 $evalscript $fullgraph $testfile $embeddings $embeddings -f 0 --random_seed 100 $additionalflags --result_file $resfile -directed 0 \&
						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
							echo "wait"
							Count=0
							fi
						fi

						embeddings1=$embeddings-large.npy
						additionalflags="--npy"
						echo python3 $evalscript $fullgraph $testfile $embeddings1 $embeddings1 -f 0 --random_seed 100 $additionalflags --result_file $resfile -directed 0 \&
						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
						embeddings1=""
						embeddings=$embeddings-small.npy
						echo python3 $evalscript $fullgraph $testfile $embeddings $embeddings -f 0 --random_seed 100 $additionalflags --result_file $resfile -directed 0 \&
						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0


					fi

					
						embeddings=""

					else
					additionalflags=""
					
					if [[ $methodname == *"GraphSAGE"* ]]; then
						additionalflags="--npy "

						for model in graphsage_seq gcn graphsage_maxpool graphsage_meanpool graphsage_maxpool n2v graphsage_mean;do
							for lr in 0.0001 0.00001; do
								additionalflags=" --node_id_file $embeddings-$model-lr$lr.embeddingsval.txt"
						if [[ -f $embeddings"-$model-lr$lr.embeddingsval.npy" ]];then
						embeddingsfile=$embeddings"-$model-lr$lr.embeddingsval.npy"
						echo python3 $evalscript $fullgraph $testfile $embeddingsfile $embeddingsfile -f 0 --random_seed 100 $additionalflags  -directed 0 --result_file $resfile \&
						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
						 sleep 2  &
						fi
						done
						done
					fi
				if [[ $methodname == *"verse"* ]];then
					additionalflags="--verse 128"
			 	fi
			 	if [[ -f $embeddings ]]; then
						echo python3 $evalscript $fullgraph $testfile $embeddings $embeddings -f 0 --random_seed 100 $additionalflags --result_file $resfile -directed 0 \&
						Count=$(expr $Count + 1)
						if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
					fi
						 sleep 2  &
						fi
					fi
		fi
			
			if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
			fi
		done
	done''')


def makeevalnc(methods, datasets):
    f = open('/home/congttn/badne/code/evaluation/eval/evalnc.sh', "w+")
    f.write('''datasetir=/data
Count=0
cores=24
for methodname in''')
    for i in range(len(methods)):
        f.write(" " + methods[i])
    
    f.write(''';
do
	for dataset in''')
    
    for i in range(len(datasets)):
        f.write(" " + datasets[i])
    
    f.write(''';
	do
		directed="--directed"
			if [[ $f == *"BlogCatalog"* || $f == *"Flickr"*  || $f == *"Reddit"* || $f == *"PPI"* || $f == *"Youtube"* || $f == *"dblp-coauthor"* ]]; then
  				directed=""
			fi
		embeddingfile=$datasetir/embeddings/NC/$methodname-$dataset-edgelist.txt.embeddings
		embadditional=""
		datasetoption=""
		if [[ $dataset == *"Cora"* ]];then
			datasetoption="-l cora"
		else
			datasetoption="-l blogcat"
		fi
		if [[ $methodname == *"node2vec"* ]];then
			for p in 0.25 0.5 1 2 4
					do
						for q in 0.25 0.5 1 2 4
						do
							embadditional=-p$p-q$q.embeddings
							if [[ -f $embeddingfile$embadditional ]];then
								echo python3 $datasetir/code/evaluation/eval/multilabel_class_cv.py ../../../data/$dataset/edgelist/$dataset-edgelist.txt ../../../data/$dataset/edgelist/$dataset-labels.csv  $embeddingfile$embadditional $datasetoption -cv 5 $directed --result_file $datasetir/embeddings/NC/nc-results.tsv \& 
								Count=$(expr $Count + 1)
								if [[ $Count -gt $cores ]]; then
										echo "wait"
									Count=0
								fi
							fi
						done
					done
			continue
		elif [[ $methodname == *"APP"* ]];then
				embadditional="-64.tgt --hub "$embeddingfile-64.src

		elif [[ $methodname == *"NetMF"* ]];then
			embadditional="-small.npy"
			if [[ -f  ../../../data/$dataset/edgelist/$dataset-edgelist.txt.matnode-ids.txt ]];then
				embadditional="-small.npy --node_id_file ../../../data/$dataset/edgelist/$dataset-edgelist.txt.matnode-ids.txt"
			fi
			echo python3 $datasetir/code/evaluation/eval/multilabel_class_cv.py ../../../data/$dataset/edgelist/$dataset-edgelist.txt ../../../data/$dataset/edgelist/$dataset-labels.csv  $embeddingfile$embadditional $datasetoption -cv 5 $directed --result_file $datasetir/embeddings/NC/nc-results.tsv \&
			Count=$(expr $Count + 1)
			embadditional="-large.npy"
			if [[ -f  ../../../data/$dataset/edgelist/$dataset-edgelist.txt.matnode-ids.txt ]];then
				embadditional="-large.npy --node_id_file ../../../data/$dataset/edgelist/$dataset-edgelist.txt.matnode-ids.txt"
			fi
		elif [[ $methodname == *"SDNE"* ]];then
			embadditional=".mat"
		elif [[ $methodname == *"DNGR"* ]];then
			embadditional=".pkl"
		elif [[ $methodname == *"LINE"* ]];then
			embadditional="-LINE2-normalized-128 -b"
			echo python3 $datasetir/code/evaluation/eval/multilabel_class_cv.py ../../../data/$dataset/edgelist/$dataset-edgelist.txt ../../../data/$dataset/edgelist/$dataset-labels.csv  $embeddingfile$embadditional $datasetoption -cv 5 $directed --result_file $datasetir/embeddings/NC/nc-results.tsv \&
			Count=$(expr $Count + 1)
			embadditional="-LINE1-normalized-128 -b"
			echo python3 $datasetir/code/evaluation/eval/multilabel_class_cv.py ../../../data/$dataset/edgelist/$dataset-edgelist.txt ../../../data/$dataset/edgelist/$dataset-labels.csv  $embeddingfile$embadditional $datasetoption -cv 5 $directed --result_file $datasetir/embeddings/NC/nc-results.tsv \& 
			Count=$(expr $Count + 1)
			embadditional="-LINE-concatenated -b"
		elif [[ $methodname == *"verse"* ]];then
			embadditional=" --verse 128"
		elif [[ $methodname == *"GraphSAGE"* ]];then
			for model in graphsage_seq gcn graphsage_maxpool graphsage_meanpool graphsage_maxpool n2v graphsage_mean;do
				for lr in 0.0001 0.00001; do
				embadditional="-$model-lr$lr.embeddingsval.npy --node_id_file $embeddingfile-$model-lr$lr.embeddingsval.txt"
				if [[ -f $embeddingfile"-$model-lr$lr.embeddingsval.npy" ]];then
					echo python3 $datasetir/code/evaluation/eval/multilabel_class_cv.py ../../../data/$dataset/edgelist/$dataset-edgelist.txt ../../../data/$dataset/edgelist/$dataset-labels.csv  $embeddingfile$embadditional $datasetoption -cv 5 $directed --result_file $datasetir/embeddings/NC/nc-results.tsv \& 
					Count=$(expr $Count + 1)
					if [[ $Count -gt $cores ]]; then
						echo "wait"
						Count=0
					fi
				fi
			done
		done

		continue

		fi
		
		
		echo python3 $datasetir/code/evaluation/eval/multilabel_class_cv.py ../../../data/$dataset/edgelist/$dataset-edgelist.txt ../../../data/$dataset/edgelist/$dataset-labels.csv  $embeddingfile$embadditional $datasetoption -cv 5 $directed --result_file $datasetir/embeddings/NC/nc-results.tsv \& 
	done
		Count=$(expr $Count + 1)
		if [[ $Count -gt $cores ]]; then
				echo "wait"
				Count=0
		fi
done''')

maketrainlp(['APP'], ['BlogCatalog'])
maketrainnc(['APP'], ['BlogCatalog'])

makeevallp(['APP'], ['BlogCatalog'])
makeevalnc(['APP'], ['BlogCatalog'])
