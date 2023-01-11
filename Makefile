CC=gcc
CFLAGS=-Wall -Itests/include -g -fPIC -std=c99

EX1_SRC=\
	ex1/flip_bit.c \
	ex1/get_bit.c \
	ex1/set_bit.c \
	tests/bit_ops_test.c

EX2_SRC=\
	ex2/lfsr_calculate.c \
	tests/lfsr_test.c

EX3_SRC=\
	ex3/vector.c \
	tests/vector_test.c

EX1_OBJ=$(EX1_SRC:.c=.o)
EX2_OBJ=$(EX2_SRC:.c=.o)
EX3_OBJ=$(EX3_SRC:.c=.o)
OBJ=$(EX1_OBJ) $(EX2_OBJ) $(EX3_OBJ)

all: bit_ops lfsr vector

bit_ops: $(EX1_OBJ)
	$(CC) $(CFLAGS) -o $@ $?

lfsr: $(EX2_OBJ)
	$(CC) $(CFLAGS) -o $@ $?

vector: $(EX3_OBJ)
	$(CC) $(CFLAGS) -o $@ $?

$(OBJ): %.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

.PHONY: clean

clean:
	rm -f $(EX1_OBJ) $(EX2_OBJ) $(EX3_OBJ) lfsr bit_ops vector
