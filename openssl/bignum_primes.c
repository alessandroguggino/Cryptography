#include <openssl/bn.h>
#include <openssl/rand.h>
#include <openssl/err.h>

int main(){
    int rc = RAND_load_file("/dev/random", 32);

    // generate a prime number: 1 success, 0 error
    BIGNUM *prime1 = BN_new();
    if(!BN_generate_prime_ex(prime1, 16, 0, NULL, NULL, NULL)){
        ERR_print_errors_fp(stderr);
        exit(1);
    }
    BN_print_fp(stdout, prime1);
    printf("\n");

    // check if it is prime number
    if(BN_is_prime_ex(prime1, 8, NULL, NULL)){
        printf("Yes, it is a prime number\n");
    }
    else{
        printf("No, it is not a prime number\n");
    }
    printf("\n");

    // generate a number not prime
    BIGNUM *prime2 = BN_new();
    BN_set_word(prime2, 128);
    BN_print_fp(stdout, prime2);
    printf("\n");

    // check if it is prime number
    if (BN_is_prime_ex(prime2, 8, NULL, NULL))
    {
        printf("Yes, it is a prime number\n");
    }
    else
    {
        printf("No, it is not a prime number\n");
    }
    printf("\n");

    // generate a random big number
    BIGNUM *rand_num = BN_new();
    BN_rand(rand_num, 32, 0, 1);
    BN_print_fp(stdout, rand_num);
    printf("\n");

    // check if it is prime number
    if (BN_is_prime_ex(rand_num, 8, NULL, NULL))
    {
        printf("Yes, it is a prime number\n");
    }
    else
    {
        printf("No, it is not a prime number\n");
    }

    return 0;
}
