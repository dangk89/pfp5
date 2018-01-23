type link = (i32, i32)

let sgm_scan_add [n] (vals:[n]f64) (flags:[n]bool): [n]f64 =
  let pairs = scan (\ (v1,f1) (v2,f2) -> (if f2 then v2 else v1 + v2, f1 || f2)) (0f64,false) (zip vals flags)
  let (res,_) = unzip pairs
  in res

-- Calculate ranks from pages without any outbound edges
-- This defaults to the page contribution / number of pages
let calculate_dangling_ranks [n] (ranks:[n]f64) (sizes:[n]i32) : *[]f64 =
  let zipped = zip sizes ranks
  let weights = map (\(size, rank) -> if size == 0 then rank else 0f64) zipped
  let total = (reduce (+) 0f64 weights) / (f64.i32 n)
  in map (+ total) ranks

-- Calculate ranks from all pages
-- A rank is counted as the contribution of a page / the outbound edges from that page
-- A contribution is defined as the rank of the page / the inbound edges
let calculate_page_ranks [n] (links:[]link) (ranks: *[n]f64) (sizes:[n]i32) : []f64 =
  let (froms, _) = unzip links
  let get_rank (idx:i32) : f64 = if sizes[idx] == 0 then 0f64 else ranks[idx] / (f64.i32 sizes[idx])
  let contributions = map (\i -> unsafe (get_rank i) / (f64.i32 sizes[i])) froms
  let froms_rotated = rotate 1 froms
  let page_flags = map (\x y -> if x == y then false else true) froms froms_rotated
  let scanned_contributions = sgm_scan_add contributions page_flags
  let indiced_contributions = map (\from c flag -> (from, c, flag)) froms scanned_contributions page_flags
  let page_contributions_flags = filter (\(_, _, flag) -> flag) indiced_contributions
  let (page_froms, page_contributions) = unzip (map (\(from, c, _) -> (from, c)) page_contributions_flags)
  in scatter ranks page_froms page_contributions

let calculate_ranks [n] (links:[]link) (ranks_in: *[n]f64) (sizes:[n]i32) (iterations:i32) : *[n]f64 =
  loop ranks = ranks_in for i < iterations do
    let ranks_pages : *[]f64 = calculate_page_ranks links ranks sizes
    in calculate_dangling_ranks ranks_pages sizes

let main [n] (links_array:[][2]i32, sizes:[n]i32, ranks_initial: *[n]f64): []f64 =
  let links = map (\l -> (l[0], l[1])) links_array
  in calculate_ranks links ranks_initial sizes 10
