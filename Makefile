ACTIVATION_ID := KO6BGT@K-1176-20231225

run:
	./src/main.py --verbose \
		--fin ./input/${ACTIVATION_ID}/pota-log.yaml \
		--fdbg ./output/${ACTIVATION_ID}/intermediate.yaml \
		--fout ./output/${ACTIVATION_ID}/${ACTIVATION_ID}.adif
