#include <stdio.h>
#include <openssl/bn.h>

int main()
{
    char num_string[] = "1234567890123456789012345678901234567890";
    BIGNUM *big_number = BN_new();
    
    BN_dec2bn(&big_number, num_string); // convertion to BIGNUM

    BN_print_fp(stdout, big_number);
    printf("\n");

    char *num_string_after_conv = BN_bn2hex(big_number); // convertion to HEX (structure allocated in heap)
    printf("%s\n", num_string_after_conv);

    // free dynamically allocated memory
    BN_free(big_number);
    OPENSSL_free(num_string_after_conv);

    return 0;
}
