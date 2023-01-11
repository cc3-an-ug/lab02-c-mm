/* Include the system headers we need */
#include <stdlib.h>
#include <stdio.h>

/* Include our header */
#include "vector.h"

/* Define what our struct is */
struct vector_t {
  size_t size;
  int *data;
};

/* Utility function to handle allocation failures. In this
   case we print a message and exit. */
static void allocation_failed() {
    fprintf(stderr, "Out of memory.\n");
    exit(1);
}

/* Create a new vector */
vector_t *vector_new() {
  vector_t *retval;

  /* First, we need to allocate the memory for the struct and check our return value to make sure we got memory*/

  /* ADD CODE HERE */

  /* Now we need to initialize our data and, again, verify that we still got memory for our return value*/

  /* ADD CODE HERE */

  return retval;
}

/* Free up the memory allocated for the passed vector */
void vector_delete(vector_t *v) {
  /* Remember, you need to free up ALL the memory that is allocated */

  /* ADD CODE HERE */
}

/* Return the value in the vector */
int vector_get(vector_t *v, size_t loc) {
  /* If we are passed a NULL pointer for our vector, complain about it and
   * exit.
   */

  /* ADD CODE HERE */

  /* If the requested location is higher than we have allocated, return 0.
   * Otherwise, return what is in the passed location.
   */

  /* ADD CODE HERE */
  return NULL;
}

/* Set a value in the vector. If the extra memory allocation fails, call allocation_failed(). */
void vector_set(vector_t *v, size_t loc, int value) {
  /* What do you need to do if the location is greater than the size we have
   * allocated?  Remember that unset locations should contain a value of 0.
   */

  /* ADD CODE HERE */
}
