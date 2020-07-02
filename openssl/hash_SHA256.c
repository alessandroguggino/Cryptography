#include <stdio.h>
#include <openssl/sha.h>
#include <openssl/err.h>

#define BUFF_SIZE 256

void handleErrors(void){
	ERR_print_errors_fp(stderr);
	abort();
}

int main(int argc, char* argv[]){
	FILE* f_in;
	unsigned char buff[BUFF_SIZE];
	int i=0, n;
	unsigned char digest[SHA256_DIGEST_LENGTH];
	SHA256_CTX context;
	
	f_in = fopen(argv[1], "r");
	if(f_in == NULL)
		handleErrors();
	
	// init
	SHA256_Init(&context);
	
	// update
	while((n = fread(buff,1,BUFF_SIZE,f_in)) > 0)
		SHA256_Update(&context, buff, n);
	
	// final
	SHA256_Final(digest, &context);
	
	fclose(f_in);

	printf("The digest is: ");
	for(i = 0; i < SHA256_DIGEST_LENGTH; i++)
		printf("%02x", digest[i]);
	printf("\n");
		
	return 0;
}
