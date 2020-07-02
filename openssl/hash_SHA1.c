#include <stdio.h>
#include <openssl/evp.h>
#include <string.h>
#include <unistd.h>

#define BUF_SIZE 1024

int main(int argc,char **argv) {
	EVP_MD_CTX *md;
	unsigned char md_value[EVP_MAX_MD_SIZE];
	int n,i,md_len;
	unsigned char buf[BUF_SIZE];
	FILE *fin;


	if(argc < 2) {
		printf("Please give a filename to compute the SHA-1 digest on\n");
		exit(1);
	}

	if((fin = fopen(argv[1],"r")) == NULL) {
		printf("Couldnt open input file, try again\n");
		exit(1);
	}

	// create
	md = EVP_MD_CTX_new();
	EVP_MD_CTX_init(md);
	
	// init: context, digest_algorithm
	EVP_DigestInit(md, EVP_sha1());
	
	// update: context, buffer, buffer_length
	while((n = fread(buf,1,BUF_SIZE,fin)) > 0)
		EVP_DigestUpdate(md, buf, n);
	
	// final: context, buffer, buffer_length
	if(EVP_DigestFinal_ex(md, md_value, &md_len) != 1) {
		printf("Digest computation problem\n");
		exit(1);
	}
	
	// free
	EVP_MD_CTX_free(md);

	printf("The digest is: ");
	for(i = 0; i < md_len; i++)
		printf("%02x", md_value[i]);
	printf("\n");

	return 0;
}
