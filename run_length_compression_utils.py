#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_length_compression_utils.py

Utilities for Run-Length compression of binary images
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.image as mpimg 
import math

decoding_dict = dict();

def NextPowerOfTwo(n):
    number = 1
    bit_count = 0;
    while number <= n: 
        bit_count += 1;
        number *= 2;

    return number, bit_count;

def RunLengthEncode(file_source, file_encoded, T = False):  
    # N1 dimension (N1_bits bits / symbol), N2 dimension (N2_bits bits / symbol), T (Transpose): NO = 0 or YES = 1 (T_bits bits / symbol), \
    #   S(start image value): black = 0 and white = 1 (S_bits bits / symbol) \
    # if S == 0: \
    #   image: n1 zeros (N_bits / symbol), n2 ones (N_bits / symbol), n3 zeros (N_bits / symbol), n4 ones (N_bits / symbol), ....\
    # if S == 1: \
    #   image: n1 ones (N_bits / symbol), n2 zeros (N_bits / symbol), n3 ones (N_bits / symbol), n4 zeros (N_bits / symbol), ....
    #
    # N1|N2|T|S|n1|n2|n3|n4|..
    
    global decoding_dict;
            
    file_source = np.array(mpimg.imread(file_source));
    file_source = file_source.astype(np.uint8);
    binary_image = file_source[:, :, 0];        
    file_encoded = open(file_encoded, "wb");
    
    T_bits = 1;
    if T:
        binary_image = binary_image.T;
        T = 1;
    else:
        T = 0; 
        
    S_bits = 1;
    if int(binary_image[0, 0]) == 0:
        S = 0;
    else:
        S = 1;
        
    binary_image = binary_image;
    N1, N2 = binary_image.shape;
    binary_image_vector = binary_image.flatten(order = 'C');
    
    a1 = binary_image_vector[1:N1 * N2];
    a2 = binary_image_vector[0:N1 * N2 - 1];
    temp = a1 + a2;   
    indx = [i for i in range(len(temp)) if temp[i] == 1];
 
    binary_image_encoded = np.array(indx + [N1 * N2 - 1]) - np.array(([-1] + indx));
    binary_image_encoded = binary_image_encoded.tolist();
 
    _, N_bits = NextPowerOfTwo(max(binary_image_encoded));
    _, N1_bits = NextPowerOfTwo(N1 - 1);
    _, N2_bits = NextPowerOfTwo(N2 - 1);
    
    
    if N1_bits > N2_bits:
        N2_bits = N1_bits;
    else:
        N1_bits = N2_bits; 
        
    if N1_bits < 10:
        N1_bits_str = '0' + str(N1_bits);
    else:
        N1_bits_str = str(N1_bits);
        
    if N2_bits < 10:
        N2_bits_str = '0' + str(N2_bits);
    else:
        N2_bits_str = str(N2_bits);
    if N_bits < 10:
        N_bits_str = '0' + str(N_bits);
    else:
        N_bits_str = str(N_bits); 
        
    T_bits_str = '01';    
    S_bits_str = '01';
    
    print(f'Encoding for N1 = {N1}: {N1_bits} [bits / symbol]');
    print(f'Encoding for N2 = {N2}: {N2_bits} [bits / symbol]');
    print(f'Encoding for T (transpose): {T_bits} [bits / symbol]');
    print(f'Encoding for S (start image value): {S_bits} [bits / symbol]');    
    print(f'Encoding for n; max(n) = {max(binary_image_encoded)}: {N_bits} [bits / symbol]\n');
    decoding_dict['N1_bits'] = N1_bits;
    decoding_dict['N2_bits'] = N2_bits;
    decoding_dict['N_bits'] = N_bits;
    
    # the actual Runlength encoding
    # add N1 and N2 dimensions, T (transpose) and S (start image value)
    code_string = ''; # bitstream (a string of 0s and 1s)
    
    codeword = format(N1 - 1, N1_bits_str + 'b'); # N1 dimension
    code_string += codeword;
    decoding_dict[codeword] = N1;
    
    codeword = format(N2 - 1, N2_bits_str + 'b'); # N2 dimension
    code_string += codeword;
    decoding_dict[codeword] = N2;
    
    codeword = format(T, T_bits_str + 'b'); # T (transpose)
    code_string += codeword;
    
    codeword = format(S, S_bits_str + 'b'); # S (start image value)
    code_string += codeword;

    # add image data
    for i in range(len(binary_image_encoded)):
        symbol = binary_image_encoded[i];
        codeword = format(symbol, N_bits_str + 'b');
        codeword = codeword.replace(' ', '0');
        decoding_dict[codeword] = symbol;
        code_string += codeword
       
    # break bitstream into the groups of 8 bits each (an integer number 0 - 255) and write these \
    #   integer number in binary format into the output file   
    n = int(8 - 8 * (len(code_string) / 8 - math.floor(len(code_string) / 8))); # n-bits are missing from the final group of 8 bits
    decoding_dict['1' * (n + 8)] = ''; # ignore end flag
    code_string = code_string + '1' * (n + 8); # add ignore end flag
    
    for i in range(int(len(code_string) / 8)): 
        eight_bits = code_string[i * 8: i * 8 + 8];
        integer = int(eight_bits, 2);
        integer_binary = integer.to_bytes(1, byteorder = 'big', signed = False);
        file_encoded.write(integer_binary);
    
    file_encoded.close();
    
    binary_image_bytes = int(N1 * N2 / 8);
    code_string_bytes = int((len(code_string) - N1_bits - N2_bits - T_bits - S_bits) / 8);
    print(f'Size of the original file: {binary_image_bytes} [bytes]')
    print(f'Size of the encoded file: {code_string_bytes} [bytes]')
    print(f'Compression ratio: {binary_image_bytes / code_string_bytes : 0.5f}\n');
    
    return None;

def RunLengthDecode(file_encoded, file_decoded):
    
    file_encoded = open(file_encoded,"rb");
    binary_string = file_encoded.read();
    file_encoded.close();
    
    code_string = ''; # bitstream (a string of 0s and 1s)
    for i in range(len(binary_string)):
        integer = binary_string[i];  
        code_string += f'{integer:08b}';
            
    # remove ignore end flag
    ignore_end_flag = '1' * 8;
    for i in range(8):
        ignore_end_flag += '1';
        if ignore_end_flag in decoding_dict:
            code_string = code_string[0:-len(ignore_end_flag)];  
            break;
        
    # the actual Runlength decoding
    # get N1 dimension
    codeword = '';
    N1_bits = decoding_dict['N1_bits'];
    for i in range(0, len(code_string), N1_bits):
     codeword = code_string[i:i + N1_bits];
     if codeword in decoding_dict:
         symbol = decoding_dict[codeword];
         N1 = symbol;
         break;
            
    # get N2 dimension
    codeword = '';
    j = i + 1;
    N2_bits = decoding_dict['N2_bits'];
    for i in range(N1_bits, len(code_string), N2_bits):
     codeword = code_string[i:i + N2_bits];
     if codeword in decoding_dict:
         symbol = decoding_dict[codeword];
         N2 = symbol;
         break;

    # get T (transpose)
    i = N1_bits + N2_bits;
    codeword = code_string[i];
    T = int(codeword);

    # get S (start image value)
    i += 1;
    codeword = code_string[i];
    S = int(codeword);    
    
    # get list of n zeros and ones
    N_bits = decoding_dict['N_bits'];
    binary_image_encoded = list();
    codeword = '';
    j = i + 1;
    for i in range(j, len(code_string), N_bits):
        codeword = code_string[i:i + N_bits];
        if codeword in decoding_dict:
            symbol = decoding_dict[codeword];
            binary_image_encoded += [symbol];
            codeword = '';
            
    # preallocate memory for image array
    image_decoded = np.zeros((N1 * N2, 1), dtype = np.uint8, order = 'C');
    pos = 0;
    for ind, val in enumerate(binary_image_encoded):
        if ind % 2 == 0:
            image_decoded[pos:pos + val] = S;
            pos += val;
        else:
            image_decoded[pos:pos + val] = int(not(S));
            pos += val;            
    
    image_decoded = image_decoded.reshape(N1, N2);
        
    if T:
        image_decoded = image_decoded.T;
       
    # generate colormap
    cmap = matplotlib.colors.ListedColormap(['black', 'white'])
    # save binary array image
    plt.imsave(file_decoded, image_decoded, cmap=cmap);
    
    return None;