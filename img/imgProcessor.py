import sys
from PIL import Image

# 定义 SHA256 算法所需的逻辑函数
# Define logical functions for SHA256
def Ch(x, y, z):
	return (x & y) ^ (~x & z)
def Maj(x, y, z):
	return (x & y) ^ (y & z) ^ (z & x)
def Sigma0(x):
	return (((x << 30) | (x >> 2)) ^ ((x << 19) | (x >> 13)) ^ ((x << 10) | (x >> 22))) & 0xffffffff
def Sigma1(x):
	return (((x << 26) | (x >> 6)) ^ ((x << 21) | (x >> 11)) ^ ((x << 7) | (x >> 25))) & 0xffffffff
def sigma0(x):
	return (((x << 25) | (x >> 7)) ^ ((x << 14) | (x >> 18)) ^ (x >> 3)) & 0xffffffff
def sigma1(x):
	return (((x << 15) | (x >> 17)) ^ ((x << 13) | (x >> 19)) ^ (x >> 10)) & 0xffffffff

if __name__ == '__main__':

	# 对图像采样并处理图像数据为 SHA256 初始数据
	img = Image.open(sys.argv[1])
	M = [[0] * 16] * 4097
	wid, hei = img.size
	for i in range(0, 255):
		for j in range(0, 255):
			colour = list(img.getpixel((int(wid * i / 256), int(hei * j / 256))))
			M[i * 16 + int(j / 16)][j % 16] = (colour[0] << 24) | (colour[1] << 16) | (colour[2] << 8)
			if len(colour) == 4: 
				M[i * 16 + int(j / 16)][j % 16] |= int(colour[3] * 255)
			else:
				M[1 * 16 + int(j / 16)][j % 16] |= 255
	M[4096][0] = 1 << 31
	M[4096][15] = 1 << 21
	# 处理后共 4096 个消息块

	# 定义 SHA256 算法初始常量
	# Define initial constants for SHA256
	H = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
	K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
		 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
		 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
		 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
		 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
		 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
		 0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
		 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

	W = [0] * 64
	for h in range(1, 4096):
		for i in range(0, 63):
			for t in range(0, 15):
				W[t] = M[i][t]
			for t in range(16, 63):
				W[t] = (sigma1(W[t-2]) + W[t-7] + sigma0(W[t-15]) + W[t-16]) & 0xffffffff
			tmpH = H
			T1 = (H[7] + Sigma1(H[4]) + Ch(H[4], H[5], H[6]) + K[i] + W[i]) & 0xffffffff
			T2 = (Sigma0(H[0]) + Maj(H[0], H[1], H[2])) & 0xffffffff
			H[7] = H[6]
			H[6] = H[5]
			H[5] = H[4]
			H[4] = H[3] + T1
			H[3] = H[2]
			H[2] = H[1]
			H[1] = H[0]
			H[0] = T1 + T2
			for t in range(0, 7):
				H[t] = (H[t] + tmpH[t]) & 0xffffffff
	
	# 输出最终哈希值
	# Output final Hash result
	for t in range(0, 7):
		if H[t] < 0x10000000: # 第一位前补零
			print('0', end ='')
			if H[t] < 0x01000000: # 第二位前补零
				print('0', end ='')
				if H[t] < 0x00100000: # 第三位前补零
					print('0', end ='')
					if H[t] < 0x00010000: # 第四位前补零
						print('0', end ='')
						if H[t] < 0x00001000: # 第五位前补零
							print('0', end ='')
							if H[t] < 0x00000100: # 第六位前补零
								print('0', end ='')
								if H[t] < 0x00000010: # 第七位前补零
									print('0', end ='') # 第八位（最后一位）不需要补零
		print(format(H[t], 'x'), end = '')
	print('\n')


# Thanks: [一文读懂 SHA256 算法原理及其实现（by Zhihu@Datacruiser​）](https://zhuanlan.zhihu.com/p/94619052)
# 附: [Visualized SHA256 Algorithm](https://sha256algorithm.com/)
