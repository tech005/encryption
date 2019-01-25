"""
Code practice By Ryan Rogers
Program makes 2 folders and a random key if nonexistant.
Run program again to encrypt/decrypt contents.
Skips folders and produces incorrect key if the original key is not present.
"""
from cryptography.fernet import Fernet, InvalidToken
import os


# generate key
def generatekey():
        key = Fernet.generate_key()
        return key


def makefilelist(path):
        files = os.listdir(path)
        return files


# encrypting files in folder
def encryptingfiles(files,key):
        for i in range(len(files)):
                filex = files[i]
                if filex.endswith(".encrypted"):
                        pass
                else:
                        try:
                                fernet = Fernet(key)
                                input_file = filex
                                output_file = filex + ".encrypted"
                                with open(input_file, 'rb') as f:
                                        data = f.read()             
                                
                                encrypted = fernet.encrypt(data)
                                with open(output_file,'wb') as f:
                                        f.write(encrypted)
                                os.remove(filex)
                        except PermissionError:
                                pass


# decrypt files in folder
def decryptingfiles(files,key):
        for i in range(len(files)):
                filex = files[i]
                if filex.endswith(".encrypted"):
                        try:
                                fernet = Fernet(key)
                                input_file = filex
                                output_file = filex[:-9]
                                with open(input_file, 'rb') as f:
                                        data = f.read()
                                        
                                decrypted = fernet.decrypt(data)
                                with open(output_file,'wb') as f:
                                        f.write(decrypted)
                                os.remove(filex)
                        except PermissionError:
                                pass
                        except InvalidToken:
                                print("Wrong key for "+filex)
                else:
                        pass
                        

# read key from key.key   
def readkey():
        file = open('key.key', 'rb')
        key = file.read()
        file.close()
        return key


# save key to file
def savekeytofile(key):
        file = open("key.key", 'wb')
        file.write(key)
        file.close()


def main():
        folders = ["ToEncrypt","ToDecrypt"]
        
        # make folders if not there
        for i in range(len(folders)):
                try:
                        os.mkdir(folders[i])
                except FileExistsError:
                        pass
        # make key if not there read if is 
        try:
                key = readkey()
        except FileNotFoundError:
                key = generatekey()
                savekeytofile(key)
                print("generating key.key!")
        # assign folders
        os.chdir(folders[0])
        encryptpath = os.getcwd()
        os.chdir("..")
        os.chdir(folders[1])
        decryptpath = os.getcwd()
        # enter folder to encrypt and encrypt if !endswith .encrypted
        os.chdir(encryptpath)
        filestoencrypt = makefilelist(encryptpath)
        encryptingfiles(filestoencrypt,key)
        os.chdir("..")
        # enter folder to decrypt and decrypt if endswith .encrypted
        os.chdir(decryptpath)
        filestodecrypt = makefilelist(decryptpath)
        decryptingfiles(filestodecrypt,key)
                
main()
           
        
        
