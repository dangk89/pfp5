type link = (i32, i32)

-- vectorer
-- Calculate ranks from pages without any outbound edges
-- This defaults to the page contribution / number of pages

--let calculate_dangling_ranks [n] (ranks:[n]f32) (sizes:[n]i32) : []f32 =
--  map(+((reduce (+) 0f32 (
--    map (\(size, rank) -> if size == 0 then rank else 0f32) 
--    (zip sizes ranks)) / (f32.i32 n)))) ranks 



let calculate_dangling_ranks [n] (ranks:[n]f32) (sizes:[n]i32) : []f32 =
  let total = (reduce (+) 0f32 (
    map (\(size, rank) -> if size == 0 then rank else 0f32) (zip sizes ranks))) / (f32.i32 n)
    in map(+ total) ranks

-- Calculate ranks from all pages
-- A rank is counted as the contribution of a page / the outbound edges from that page
-- A contribution is defined as the rank of the page / the inbound edges
let calculate_page_ranks [n] (links:[]link) (ranks: [n]f32) (sizes:[n]i32) : []f32 =
  let get_rank (idx:i32) : f32 = if sizes[idx] == 0 then 0f32 else ranks[idx] / (f32.i32 sizes[idx]) --  Pagerank A (n page that point to A) / (n links out of page A)
  let contribution = map (\(from, _) -> unsafe (get_rank from)) links  --
  let get_contributions (r_idx: i32) = reduce (+) 0f32 (map (\c_idx -> 
    if c_idx == r_idx then
      contribution[c_idx] 
    else 0f32) (iota (length contribution)))  ---
  let new_ranks = map get_contributions (iota n)
  in map (\idx -> ranks[idx] + new_ranks[idx] / (f32.i32 n)) (iota n)
    
let calculate_ranks [n] (links:[]link) (ranks_in: [n]f32) (sizes:[n]i32) (iterations:i32) : []f32 = 
  loop ranks_next = ranks_in for i < iterations do
    let ranks_pages = calculate_page_ranks links ranks_next sizes
    in calculate_dangling_ranks ranks_pages sizes

let main (from:[]i32, to:[]i32, sizes:[]i32): []f32 =
  let n_links = length from                                               -- outbound links
  let n_pages = length sizes
  let links = map (\idx -> (from[idx], to[idx])) (iota n_links)          -- p1, send to 165 (1,165)
  let ranks_initial = map (\_ -> 1f32 / (f32.i32 n_pages)) (iota n_pages) -- damping/ number of web pages
  in calculate_ranks links ranks_initial sizes 10
