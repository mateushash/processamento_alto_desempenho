#include <mpi.h>

void main(int argc, char **argv) {
    int rank, size;

    MPI_Init(&argc, &argv); // Initialize the MPI environment
    MPI_Comm_rank(MPI_COMM_WORLD, &rank); // Get the rank of the process
    MPI_Comm_size(MPI_COMM_WORLD, &size); // Get the number of processes

    printf("Hello world from process %d of %d\n", rank, size);

    MPI_Finalize(); // Finalize the MPI environment
}
