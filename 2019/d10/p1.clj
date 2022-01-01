(defn parse-input [input]
  (let [grid (clojure.string/split input #"\n")
        width (count (get grid 0))
        height (count grid)] 
    (filter identity 
      (for [x (range width) y (range height)]
           (when (= \# (get (grid y) x)) (list x y))))))

(defn direction [a b]
  (let [d (Math/atan2 (- (first b) (first a)) (- (last b) (last a)))]
    (mod d (* 2 Math/PI))))

(defn count-visible [u a]
  (count (set (map #(direction a %) (remove #(= a %) u)))))

(defn count-visible-all [u]
  (for [a u] (count-visible u a)))

(defn pp [x] (prn x) x)

(as-> (slurp "input") $
  (parse-input $)
  (count-visible-all $)
  (apply max $)
  (prn $))
