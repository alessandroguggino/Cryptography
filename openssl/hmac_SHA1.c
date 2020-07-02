#include <stdio.h>
#include <string.h>
#include <openssl/hmac.h>
#include <openssl/err.h>

#define KEY "deadbeefdeadbeef"

#define BUF_SIZE 1024

void handleErrors(void)
{
	ERR_print_errors_fp(stderr);
	abort();
}


int main(int argc,char **argv) {
	HMAC_CTX *hmac_ctx;

	int n,i,len;
	unsigned char buf[1024],hmac_value[1024];

	FILE *fin;

	if(argc < 2) {
		printf("Please give a filename to compute the HMAC on\n");
		return 1;
	}

	if((fin = fopen(argv[1],"r")) == NULL) {
		printf("Couldnt open input file, try again\n");
		exit(1);
	}

	// create
	if((hmac_ctx = HMAC_CTX_new()) == NULL)
		handleErrors();
	
	// init: context, key, ley_length, digest_algorithm
	if(1!=HMAC_Init_ex(hmac_ctx,KEY,strlen(KEY),EVP_sha1(),NULL))
		handleErrors();

	// update: context, buffer, buffer_length
	while((n = fread(buf,1,BUF_SIZE,fin)) > 0)
		if(1!=HMAC_Update(hmac_ctx, buf,n))
			handleErrors();

	// final: context, buffer, buffer_length
	if(1!=HMAC_Final(hmac_ctx, hmac_value, &len))
		handleErrors();
	
	// free
	HMAC_CTX_free(hmac_ctx);

	printf("MAC is: ");
	for(i = 0; i < len; i++)
		printf("%02x", hmac_value[i]);
	printf("\n");

	return 0;
}
