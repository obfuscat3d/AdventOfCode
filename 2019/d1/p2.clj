(defn fuel [m] (- (int (/ m 3)) 2))

(defn fuelr [m]
  (if (< m 9) 
    0 
    (let 
      [f (fuel m)]
      (+ f (fuelr f)))))

(prn
  (->> "input"
  slurp
  clojure.string/split-lines
  (map #(Integer/parseInt %))
  (map #(fuelr %))
  (reduce +)))
