#include <openssl/bn.h>
#include <openssl/err.h>

int main(){
    BIGNUM *a = BN_new();
    BIGNUM *b = BN_new();
    BIGNUM *res = BN_new();
    BN_CTX *ctx = BN_CTX_new();

    BN_set_word(a, 8);
    BN_set_word(b, 14);

    // add
    printf("add: %d + %d =\n", BN_get_word(a), BN_get_word(b));
    BN_add(res, a, b);
    BN_print_fp(stdout, res);
    printf("\n");
    printf("%d\n", BN_get_word(res));

    // sub
    printf("sub: %d - %d =\n", BN_get_word(b), BN_get_word(a));
    BN_sub(res, b, a);
    BN_print_fp(stdout, res);
    printf("\n");
    printf("%d\n", BN_get_word(res));

    // div
    BIGNUM *div = BN_new();
    BIGNUM *rem = BN_new();
	printf("div: %d / %d =\n", BN_get_word(b), BN_get_word(a));
    BN_div(div, rem, b, a, ctx);
    printf("div=%d, rem=%d\n", BN_get_word(div), BN_get_word(rem));

    // mod exp
    BIGNUM *m = BN_new();
    BN_set_word(m, 35);
    printf("mod exp: %d ^ %d mod %d =\n", BN_get_word(a), BN_get_word(b), BN_get_word(m));
    if(!BN_mod_exp(res, a, b, m, ctx)){
        ERR_print_errors_fp(stderr);
        exit(1);
    }
    BN_print_fp(stdout, res);
    printf("\n");
    printf("%d\n", BN_get_word(res));
    
    return 0;
}
