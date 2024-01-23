# EVENT_ID      := 20231225-mount-diablo-sp
# ACTIVATION_ID := KO6BGT@K-1176-20231225

EVENT_ID      := 20240121-mount-tam-sp
ACTIVATION_ID := KO6BGT@K-1178-20240121

run:
	./src/main.py --verbose \
		--fin ./data/${EVENT_ID}/input.yaml \
		--fdbg ./data/${EVENT_ID}/debug.yaml \
		--fout ./data/${EVENT_ID}/${ACTIVATION_ID}.adi

.PHONY: test-python
test-python:
	./src/utc_offset_test.py
