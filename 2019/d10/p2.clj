; From part 1
(def asteroid-base '(31 20))

(defn parse-input [input]
  (let [grid (clojure.string/split input #"\n")]
    (filter identity 
      (for [x (range (count (get grid 0))) y (range (count grid))]
           (when (= \# (get (grid y) x)) (list x y))))))

(defn direction [a]
  (let [d (Math/atan2 (first a) (* -1 (last a)))]
    (mod d (* 2 Math/PI))))

(defn normalize [u a]
  (map 
    #(list (- (first %) (first a)) (- (last %) (last a))) 
    (remove #(= a %) u)))

; distance sort
(defn dist-sort [a b]
  (< (+ (* (first a) (first a)) (* (last a) (last a)))
     (+ (* (first b) (first b)) (* (last b) (last b)))))

; (sorted-map of direction to a sorted list of asteroids in that direction
(defn asteroids-by-direction [u]
  (loop [axd (sorted-map)
         cur (first u)
         rem (rest u)]
    (if (not cur) 
      axd
      (let [d (direction cur)]
        (recur (if (contains? axd d)
                   (assoc axd d (sort dist-sort (conj (axd d) cur)))
                   (assoc axd d (list cur)))                 
               (first rem)
               (rest rem))))))

(as-> (slurp "input") $
  (parse-input $)
  (normalize $ asteroid-base)
  (asteroids-by-direction $)
  (doseq [a (seq $)] (prn a)))

;; I got a little lazy here since we never have to sweep the full
;; circle with our laser. Instead I just printed this out, piped
;; into cat -b and read the 200th line: (-26,-3). Add back in our 
;; starting coords, (31,20) to get the answer, (5,17).

