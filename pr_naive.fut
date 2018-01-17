
type link = (i32, i32)

let main(from:[]i32, to:[]i32, sizes:[]i32): i32 = length from

-- Add contributions from pages without any outbound edges
-- This defaults to the page contribution / number of pages
let contribution_dangle [n] (ranks:[n]f32, sizes:[n]i32) : []f32 = 
  let zipped = zip sizes ranks
  let weights = map (\(size, rank) -> if size == 0 then rank else 0f32) zipped
  let total = (reduce (+) 0f32 weights) / (f32.i32 n)
  in map (+ total) ranks

-- Add contributions from pages
let contribution [n] (links:[]link, ranks: [n]f32, sizes:[n]i32) : []f32 = ranks
