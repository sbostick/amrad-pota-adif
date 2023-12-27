EVENT_ID      := 20231225-MOUNT-DIABLO
ACTIVATION_ID := KO6BGT@K-1176-20231225

run:
	./src/main.py --verbose \
		--fin ./data/${EVENT_ID}/pota-log.yaml \
		--fdbg ./data/${EVENT_ID}/intermediate.yaml \
		--fout ./data/${EVENT_ID}/${ACTIVATION_ID}.adif
