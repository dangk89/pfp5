
type link = (i32, i32)

-- Calculate ranks from pages without any outbound edges
-- This defaults to the page contribution / number of pages
let rank_dangle [n] (ranks:[n]f32, sizes:[n]i32) : []f32 = 
  let zipped = zip sizes ranks
  let weights = map (\(size, rank) -> if size == 0 then rank else 0f32) zipped
  let total = (reduce (+) 0f32 weights) / (f32.i32 n)
  in map (+ total) ranks

-- Calculate ranks from all pages
-- A rank is counted as the contribution of a page / the outbound edges from that page
-- A contribution is defined as the rank of the page / the inbound edges
let rank_page [n] (links:[]link) (ranks: [n]f32) (sizes:[n]i32) : []f32 =
  let get_rank (idx:i32) : f32 = if sizes[idx] == 0 then 0f32 else ranks[idx] / (f32.i32 sizes[idx])
  let contribution = map (\(from, _) -> unsafe (get_rank from)) links
  let get_contributions (r_idx:i32) = reduce (+) 0f32 (map (\c_idx -> 
    if c_idx == r_idx then
      contribution[c_idx] 
    else 0f32) (iota (length contribution)))
  let new_ranks = map get_contributions (iota n)
  in map (\idx -> ranks[idx] + new_ranks[idx]) (iota n)
    
let main (from:[]i32, to:[]i32, sizes:[]i32): f32 =
  let n_links = length from
  let n_pages = length sizes
  let links = map (\idx -> (from[idx], to[idx])) (iota n_links)
  let ranks_initial = map (\_ -> 0.85f32) (iota n_pages)
  let ranks = rank_page links ranks_initial sizes
  in reduce (+) 0f32 ranks

