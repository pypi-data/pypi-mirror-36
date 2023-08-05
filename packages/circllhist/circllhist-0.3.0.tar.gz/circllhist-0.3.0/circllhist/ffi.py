from cffi import FFI
ffi = FFI()
ffi.cdef("""
/** \file circllhist.h */
/*
 * Copyright (c) 2016, Circonus, Inc. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 *
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above
 *       copyright notice, this list of conditions and the following
 *       disclaimer in the documentation and/or other materials provided
 *       with the distribution.
 *     * Neither the name Circonus, Inc. nor the names of its contributors
 *       may be used to endorse or promote products derived from this
 *       software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
/*! \mainpage A C implementation of Circonus log-linear histograms
* \ref circllhist.h
*/
typedef long int ssize_t;
typedef struct histogram histogram_t;
typedef struct hist_rollup_config hist_rollup_config_t;
typedef struct hist_bucket {
  int8_t val; 
  int8_t exp; 
} hist_bucket_t;
typedef struct hist_allocator {
  void *(*malloc)(size_t);
  void *(*calloc)(size_t, size_t);
  void (*free)(void *);
} hist_allocator_t;
double hist_bucket_to_double(hist_bucket_t hb);
double hist_bucket_midpoint(hist_bucket_t in);
double hist_bucket_to_double_bin_width(hist_bucket_t hb);
hist_bucket_t double_to_hist_bucket(double d);
hist_bucket_t int_scale_to_hist_bucket(int64_t value, int scale);
int hist_bucket_to_string(hist_bucket_t hb, char *buf);
histogram_t * hist_alloc(void);
histogram_t * hist_alloc_nbins(int nbins);
/*! Fast allocations consume 2kb + N * 512b more memory
 *  where N is the number of used exponents.  It allows for O(1) increments for
 *  prexisting keys, uses default allocator */
histogram_t * hist_fast_alloc(void);
histogram_t * hist_fast_alloc_nbins(int nbins);
histogram_t * hist_clone(histogram_t *other);
histogram_t * hist_alloc_with_allocator(hist_allocator_t *alloc);
histogram_t * hist_alloc_nbins_with_allocator(int nbins, hist_allocator_t *alloc);
/*! Fast allocations consume 2kb + N * 512b more memory
 *  where N is the number of used exponents.  It allows for O(1) increments for
 *  prexisting keys, uses custom allocator */
histogram_t * hist_fast_alloc_with_allocator(hist_allocator_t *alloc);
histogram_t * hist_fast_alloc_nbins_with_allocator(int nbins, hist_allocator_t *alloc);
histogram_t * hist_clone_with_allocator(histogram_t *other, hist_allocator_t *alloc);
void hist_free(histogram_t *hist);
/*! Inserting double values converts from IEEE double to a small static integer
 *  base and can suffer from floating point math skew.  Using the intscale
 *  variant is more precise and significantly faster if you already have
 *  integer measurements. */
uint64_t hist_insert(histogram_t *hist, double val, uint64_t count);
uint64_t hist_remove(histogram_t *hist, double val, uint64_t count);
uint64_t hist_insert_raw(histogram_t *hist, hist_bucket_t hb, uint64_t count);
int hist_bucket_count(const histogram_t *hist);
int hist_num_buckets(const histogram_t *hist);
uint64_t hist_sample_count(const histogram_t *hist);
int hist_bucket_idx(const histogram_t *hist, int idx, double *v, uint64_t *c);
int hist_bucket_idx_bucket(const histogram_t *hist, int idx, hist_bucket_t *b, uint64_t *c);
int hist_accumulate(histogram_t *tgt, const histogram_t * const *src, int cnt);
int hist_subtract(histogram_t *tgt, const histogram_t * const *src, int cnt);
void hist_clear(histogram_t *hist);
uint64_t hist_insert_intscale(histogram_t *hist, int64_t val, int scale, uint64_t count);
ssize_t hist_serialize(const histogram_t *h, void *buff, ssize_t len);
ssize_t hist_deserialize(histogram_t *h, const void *buff, ssize_t len);
ssize_t hist_serialize_estimate(const histogram_t *h);
ssize_t hist_serialize_b64(const histogram_t *h, char *b64_serialized_histo_buff, ssize_t buff_len);
ssize_t hist_deserialize_b64(histogram_t *h, const void *b64_string, ssize_t b64_string_len);
ssize_t hist_serialize_b64_estimate(const histogram_t *h);
histogram_t * hist_compress_mbe(histogram_t *h, int8_t mbe);
double hist_approx_mean(const histogram_t *);
double hist_approx_sum(const histogram_t *);
double hist_approx_stddev(const histogram_t *);
double hist_approx_moment(const histogram_t *hist, double k);
uint64_t hist_approx_count_below(const histogram_t *hist, double threshold);
uint64_t hist_approx_count_above(const histogram_t *hist, double threshold);
uint64_t hist_approx_count_nearby(const histogram_t *hist, double value);
int hist_approx_quantile(const histogram_t *, const double *q_in, int nq, double *q_out);
""")
C = None
for path in [ # Search for libcircllhist.so
   "/opt/circonus/lib/libcircllhist.so", # 1. vendor path
   "./libcircllhist.so", # 2. cwd
   "libcircllhist.so" # 3. system paths via ld.so
   ]:
   try:
     C = ffi.dlopen(path)
     break
   except OSError:
     pass
if not C:
   # let dlopen throw it's error
   print("""

libcircllhist.so was not found on your system.
Please install libcircllhist from: https://github.com/circonus-labs/libcircllhist/

   """)
   ffi.dlopen("libcircllhist.so")
