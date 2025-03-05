CC=gcc
CFLAGS=-Wall -Itests/include -g -fPIC -std=c99
ACFLAGS=-Wall -Itests/autograder/include -g -fPIC -std=c99

EX1_SRC=\
	ex1/flip_bit.c \
	ex1/get_bit.c \
	ex1/set_bit.c

EX1_TEST_SRC=\
	tests/bit_ops_test.c

EX1_A_SRC=\
	tests/autograder/bit_ops_test.c

EX2_SRC=\
	ex2/lfsr_calculate.c

EX2_TEST_SRC=\
	tests/lfsr_test.c

EX2_A_SRC=\
	tests/autograder/lfsr_test.c

EX3_SRC=\
	ex3/vector.c

EX3_TEST_SRC=\
	tests/vector_test.c

EX3_A_SRC=\
	tests/autograder/vector_test.c


# Main objects
EX1_OBJ=$(EX1_SRC:.c=.o)
EX2_OBJ=$(EX2_SRC:.c=.o)
EX3_OBJ=$(EX3_SRC:.c=.o)
OBJ=$(EX1_OBJ) $(EX2_OBJ) $(EX3_OBJ)

# Test objects
EX1_TEST_OBJ=$(EX1_TEST_SRC:.c=.o)
EX2_TEST_OBJ=$(EX2_TEST_SRC:.c=.o)
EX3_TEST_OBJ=$(EX3_TEST_SRC:.c=.o)
OBJ_TEST=$(EX1_TEST_OBJ) $(EX2_TEST_OBJ) $(EX3_TEST_OBJ)

# Autograder objects
EX1_A_OBJ=$(EX1_A_SRC:.c=.o)
EX2_A_OBJ=$(EX2_A_SRC:.c=.o)
EX3_A_OBJ=$(EX3_A_SRC:.c=.o)
OBJ_A=$(EX1_A_OBJ) $(EX2_A_OBJ) $(EX3_A_OBJ)

# Conversion objects
EX1_CONV_SRC=$(EX1_SRC:.c=_conv.c)
EX2_CONV_SRC=$(EX2_SRC:.c=_conv.c)
EX3_CONV_SRC=$(EX3_SRC:.c=_conv.c)
CONV=$(EX1_CONV_SRC) $(EX2_CONV_SRC) $(EX3_CONV_SRC)

all: bit_ops lfsr vector bit_ops_autograder lfsr_autograder vector_autograder

bit_ops: $(EX1_OBJ) $(EX1_TEST_OBJ)
	$(CC) $(CFLAGS) -o $@ $?

bit_ops_autograder: $(EX1_OBJ) $(EX1_A_OBJ)
	$(CC) $(ACFLAGS) -o $@ $?

lfsr: $(EX2_OBJ) $(EX2_TEST_OBJ)
	$(CC) $(CFLAGS) -o $@ $?

lfsr_autograder: $(EX2_OBJ) $(EX2_A_OBJ)
	$(CC) $(ACFLAGS) -o $@ $?

vector: $(EX3_OBJ) $(EX3_TEST_OBJ)
	$(CC) $(CFLAGS) -o $@ $?

vector_autograder: $(EX3_OBJ) $(EX3_A_OBJ)
	$(CC) $(ACFLAGS) -o $@ $?

$(OBJ): %.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(OBJ_TEST): %.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(OBJ_A): %.o: %.c
	$(CC) $(ACFLAGS) -c -o $@ $<

$(CONV): %_conv.c: %.c
	$(CC) $(ACFLAGS) -Itests/autograder/fake -E $< > $@

.PHONY: clean

clean:
	rm -f $(OBJ) $(OBJ_TEST) $(OBJ_A) lfsr bit_ops vector lfsr_autograder bit_ops_autograder vector_autograder
