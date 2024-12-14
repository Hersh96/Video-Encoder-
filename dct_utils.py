import cv2
import numpy as np

def rgb_to_ycrcb(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

def ycrcb_to_rgb(frame):
    return cv2.cvtColor(frame, cv2.COLOR_YCrCb2BGR)

def block_dct(block):
    return cv2.dct(block)

def block_idct(block):
    return cv2.idct(block)

def quantize_block(block, quant_factor=50.0):
    q = (100 - quant_factor) / 50.0 + 1e-5
    return np.round(block / q).astype(np.int16)

def dequantize_block(block, quant_factor=50.0):
    q = (100 - quant_factor) / 50.0 + 1e-5
    return block * q

def process_frame_dct(frame, block_size=8, quant_factor=50.0):
    ycrcb = rgb_to_ycrcb(frame)
    channels = cv2.split(ycrcb)
    compressed_channels = []

    for ch in channels:
        h, w = ch.shape
        dct_blocks = []
        for row in range(0, h, block_size):
            for col in range(0, w, block_size):
                block = ch[row:row+block_size, col:col+block_size]
                if block.shape != (block_size, block_size):
                    padded = np.zeros((block_size, block_size), dtype=np.float32)
                    padded[:block.shape[0], :block.shape[1]] = block
                    block = padded
                block = np.float32(block)
                dct_b = block_dct(block)
                q_b = quantize_block(dct_b, quant_factor)
                dct_blocks.extend(q_b.flatten().tolist())
        compressed_channels.append(dct_blocks)

    return compressed_channels, ycrcb.shape

def reconstruct_frame_dct(channels_data, shape, block_size=8, quant_factor=50.0):
    h, w, _ = shape
    recons_channels = []
    for ch_data in channels_data:
        ch_data = np.array(ch_data, dtype=np.int16)
        nb_w = w // 8
        nb_h = h // 8
        ch = np.zeros((h, w), dtype=np.float32)

        idx = 0
        for row in range(nb_h):
            for col in range(nb_w):
                block_flat = ch_data[idx:idx+block_size*block_size]
                idx += block_size*block_size
                block = block_flat.reshape((block_size, block_size))
                dq_b = dequantize_block(block, quant_factor)
                idct_b = block_idct(np.float32(dq_b))
                ch[row*block_size:row*block_size+block_size, col*block_size:col*block_size+block_size] = idct_b

        recons_channels.append(ch.clip(0,255).astype(np.uint8))

    ycrcb = cv2.merge(recons_channels)
    rgb = ycrcb_to_rgb(ycrcb)
    return rgb
