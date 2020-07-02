#include <stdio.h>
#include <openssl/evp.h>
#include <openssl/sha.h>
#include <string.h>

#define BUF_SIZE 1024

int conv_hexstring(char *hexstring, char *digest){
	int i,byte;
	for(i = 0; i < SHA256_DIGEST_LENGTH; i++) {
		sscanf(hexstring+2*i, "%2X", &byte);
		digest[i] = (char)byte;
	}
	return i;
}

int main(int argc,char **argv) {

	EVP_MD_CTX *mdctx;
	unsigned char md_value[EVP_MAX_MD_SIZE];
	FILE *fin;
	int n,i,md_len;
	unsigned char buf[BUF_SIZE];
	unsigned char input_md[EVP_MAX_MD_SIZE];


	if(argc < 3) {
		printf("Please give the digest and the filename to compute the SHA-256 digest on\n");
		exit(1);
	}

	if((fin = fopen(argv[2],"r")) == NULL) {
		printf("Couldnt open input file, try again\n");
		exit(1);
	}

	if(strlen(argv[1]) != 2*SHA256_DIGEST_LENGTH){
		printf("Invalid hash length for the input.\n");
		exit(1);
	}

	conv_hexstring(argv[1],input_md);
	
	// create context
	if((mdctx = EVP_MD_CTX_new()) == NULL){
		printf("Error during context creation.\n");
		exit(1);
	}
	// init context
	if(1 != EVP_MD_CTX_init(mdctx)){
		printf("Error when initializing the context.\n");
		exit(1);
	}
	// init digest
	if(1!=EVP_DigestInit_ex(mdctx, EVP_sha256(), NULL)) {
		printf("Error when initializing the digest.\n");
		exit(1);
	}
	// update digest
	while((n = fread(buf,1,BUF_SIZE,fin)) > 0){
		if(1!=EVP_DigestUpdate(mdctx, buf, n)){
			printf("Error when updating the digest.\n");
			exit(1);
		}
	}
	// final digest
	if(1!=EVP_DigestFinal_ex(mdctx, md_value, &md_len)) {
		printf("Digest finalization problem\n");
		exit(1);
	}
	
	// free context
	EVP_MD_CTX_free(mdctx);

	printf("The digest is: ");
	for(i = 0; i < md_len; i++)
		printf("%02x", md_value[i]);
	printf("\n");
	
	// hash verification
	if(CRYPTO_memcmp(md_value, input_md, md_len)!=0)
		printf("The digests are different!\n");
	else
		printf("Same digest. Content identical.\n");

	return 0;
}
