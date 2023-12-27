EVENT_ID      := 20231225-Mount-Diablo
ACTIVATION_ID := KO6BGT@K-1176-20231225

run:
	./src/main.py --verbose \
		--fin ./data/${EVENT_ID}/input.yaml \
		--fdbg ./data/${EVENT_ID}/debug.yaml \
		--fout ./data/${EVENT_ID}/${ACTIVATION_ID}.adi
