
(defn not-decreasing [x]
  (if (< x 10)
    true
    (and (>= (mod x 10) (mod (int (/ x 10)) 10)) 
         (not-decreasing (int (/ x 10))))))

(defn dupe-digit [x]
  (if (< x 10)
    false
    (or (= (mod x 10) (mod (int (/ x 10)) 10)) 
         (dupe-digit (int (/ x 10))))))

(defn p [x] (prn x) x)

;; There has to be a way to do this with regexes
(defn single-dupe-digit [x] 
  (->> (clojure.string/split (str x) #"")
    (partition-by identity)
    (filter #(= 2 (count %)))
    count
    (< 0)))

(defn valid-pw-1 [x] (and (not-decreasing x) (dupe-digit x)))
(defn valid-pw-2 [x] (and (not-decreasing x) (single-dupe-digit x)))

(def low 137683)
(def high 596253)
(prn (count (filter #(valid-pw-1 %) (range low high) ) ) )
(prn (count (filter #(valid-pw-2 %) (range low high) ) ) )