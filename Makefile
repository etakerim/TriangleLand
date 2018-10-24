GOFMT_FILES?=$$(find . -name '*.go' |grep -v vendor)

test: fmt

run:
	@go run *.go

fmt:
	@gofmt -w $(GOFMT_FILES)

vendor:
	@go mod vendor

vet:
	@echo "go vet ."
	@go vet $$(go list ./... | grep -v vendor/) ; if [ $$? -eq 1 ]; then \
		echo ""; \
		echo "Vet found suspicious constructs. Please check the reported constructs"; \
		echo "and fix them if necessary before submitting the code for review."; \
		exit 1; \
fi
