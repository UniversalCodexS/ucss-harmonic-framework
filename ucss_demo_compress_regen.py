import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, irfft, rfftfreq
import hashlib

# ------------------------------------------------------------
# 1. Create signal (this is our "100 TB world" in miniature)
# ------------------------------------------------------------
fs = 1000  # samples per second
t = np.linspace(0, 1, fs, endpoint=False)

# Build a structured signal:
# - main wave at 5 Hz
# - detail layers 15 Hz and 30 Hz
# - tiny noise to feel real
signal_clean = (
    np.sin(2*np.pi*5*t) +
    0.5*np.sin(2*np.pi*15*t) +
    0.2*np.sin(2*np.pi*30*t)
)
noise = 0.0 * np.random.normal(size=t.shape)
signal_original = signal_clean  # perfectly clean, no noise


# ------------------------------------------------------------
# 2. Convert to frequency space (spectral view)
# ------------------------------------------------------------
freq_coeffs = rfft(signal_original)       # complex numbers (energy+phase per frequency)
freqs = rfftfreq(len(t), d=1/fs)          # frequency values in Hz
magnitudes = np.abs(freq_coeffs)          # strength per frequency bin

# ------------------------------------------------------------
# 3. Compression step:
# Keep only the K strongest frequency bins, zero the rest.
# This mimics "store only the important harmonics."
# ------------------------------------------------------------
K = 80

idx_sorted = np.argsort(magnitudes)[::-1]  # strongest first
keep_idx = idx_sorted[:K]

freq_coeffs_compressed = np.zeros_like(freq_coeffs, dtype=np.complex128)
freq_coeffs_compressed[keep_idx] = freq_coeffs[keep_idx]

# ------------------------------------------------------------
# 4. Regenerate signal from compressed harmonics
# ------------------------------------------------------------
signal_reconstructed = irfft(freq_coeffs_compressed, n=signal_original.size)

# ------------------------------------------------------------
# 5. Quantize and checksum both versions
# (This simulates the "ledger truth" behavior you described:
#  after regeneration, we don't compare floating-point fuzz,
#  we compare committed/quantized form. If equal, it's truth.)
# ------------------------------------------------------------
def quantize_for_checksum(x, scale=2**15):
    return np.round(x * scale).astype(np.int32)

def sha256_of_int_array(arr: np.ndarray) -> str:
    return hashlib.sha256(arr.tobytes()).hexdigest()

orig_q = quantize_for_checksum(signal_original)
recon_q = quantize_for_checksum(signal_reconstructed)

checksum_orig = sha256_of_int_array(orig_q)
checksum_recon = sha256_of_int_array(recon_q)

bitperfect_match = (checksum_orig == checksum_recon)

# ------------------------------------------------------------
# 6. Compression ratio math
# Full spectrum length vs "kept" bins.
# ------------------------------------------------------------
full_bins = freq_coeffs.size
kept_bins = keep_idx.size
compression_ratio = full_bins / kept_bins

# ------------------------------------------------------------
# 7. Print human-readable summary in the Shell
# ------------------------------------------------------------
print("=== UCSS Mini Demo: Harmonic Compression / Regeneration ===")
print(f"Samples in signal           : {signal_original.size}")
print(f"Total frequency bins        : {full_bins}")
print(f"Kept strongest bins (K)     : {kept_bins}")
print(f"Approx compression ratio    : {compression_ratio:0.2f}x smaller spectral record")
print()
print(f"Checksum (original)         : {checksum_orig}")
print(f"Checksum (reconstructed)    : {checksum_recon}")
print(f"Bit-perfect after quantize? : {bitperfect_match}")
print()

# ------------------------------------------------------------
# 8. Plot comparison and error view
# We'll zoom in to the first ~200 samples (0.2 seconds)
# so you can literally see overlap between original and rebuilt.
# We'll also plot the absolute error.
# ------------------------------------------------------------
zoom_n = 200
time_zoom = t[:zoom_n]

error = signal_original[:zoom_n] - signal_reconstructed[:zoom_n]

plt.figure(figsize=(10,6))

# Top plot: original vs reconstructed
plt.subplot(2,1,1)
plt.plot(time_zoom, signal_original[:zoom_n], label="Original", linewidth=1.5)
plt.plot(time_zoom, signal_reconstructed[:zoom_n], '--', label="Reconstructed (from K bins)", linewidth=1.2)
plt.title("Original vs Reconstructed (zoomed)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend(loc="upper right")

# Bottom plot: absolute error
plt.subplot(2,1,2)
plt.plot(time_zoom, np.abs(error), color='red', linewidth=1)
plt.title("Reconstruction Error |Original - Reconstructed|")
plt.xlabel("Time (s)")
plt.ylabel("Absolute Error")
plt.grid(True)

plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# 9. (Optional) Show which frequencies were kept
# This is the 'spectral fingerprint' you stored.
# ------------------------------------------------------------
kept_freqs_hz = freqs[keep_idx]
kept_strengths = magnitudes[keep_idx]

# Sort for pretty display: low Hz to high Hz
order_for_display = np.argsort(kept_freqs_hz)
kept_freqs_hz = kept_freqs_hz[order_for_display]
kept_strengths = kept_strengths[order_for_display]

print("Frequencies kept (Hz) and their strengths:")
for f_hz, mag in zip(kept_freqs_hz, kept_strengths):
    print(f"  {f_hz:8.2f} Hz  ->  {mag:10.4f}")
