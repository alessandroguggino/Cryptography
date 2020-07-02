#include <openssl/bn.h>

int main() {
    BIGNUM *b1 = BN_new();
    BIGNUM *b2 = BN_new();
    BIGNUM *b3 = BN_new();

    BN_CTX *ctx = BN_CTX_new();

    // after initialisation value is 0
    BN_print_fp(stdout, b1);
    printf("\n");

    // how to assign values
    BN_set_word(b1, 354); // word means at most a long
    BN_set_word(b2, 75);
    BN_print_fp(stdout, b1);
    printf("\n");
    BN_print_fp(stdout, b2);
    printf("\n");

    // simple operations
    BN_mod(b3, b1, b2, ctx);
    BN_print_fp(stdout, b3);
    printf("\n");

    // after usage free the memory
    BN_free(b1);
    BN_free(b2);
    BN_free(b3);

    BN_CTX_free(ctx);

    return 0;
}
