cc := g++
cflags := -std=c++17 -pipe -Wall -Ofast -Isrc/

source := src/*.cc
headers := src/*.h
target := bin/comparison

$(target): $(headers) $(source)
	@mkdir -p bin/
	$(cc) $(cflags) $(source) -o $@

.PHONY: run, clean
run: $(target)
	@./$(target)

clean:
	rm -r bin/
