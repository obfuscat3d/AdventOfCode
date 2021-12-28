;; state = (line, current-position)
;; current-position = (x y)
;; line = all points in line, [(x1 y1) (x2 y2) ...]
;; instruction = (direction distance)

(defn k [x y] (str x "," y))
(defn v [k] 
  (let [x (Integer/parseInt (first (clojure.string/split k #",")))
        y (Integer/parseInt (last (clojure.string/split k #",")))]
  (list x y)))

(defn move [state dx dy n]
  (loop [line (first state)
         pos (last state)
         n n]
    (if (= n 0)
        (list line pos)
        (recur (conj line (k (+ dx (first pos)) (+ dy (last pos))))
               (list (+ dx (first pos)) (+ dy (last pos)))
               (- n 1)))))

(defn up [state n] (move state 0 1 n))
(defn down [state n] (move state 0 -1 n))
(defn left [state n] (move state -1 0 n))
(defn right [state n] (move state 1 0 n))
(defn segment [state ins]
  (case (first ins)
    "U" (up state (last ins))
    "D" (down state (last ins))
    "L" (left state (last ins))
    "R" (right state (last ins))))

(defn manhattan-distance [p1 p2] 
  (+ (Math/abs (- (first p1) (first p2)))
     (Math/abs (- (last p1) (last p2)))))

(defn create-line [instructions]
  (loop [instructions instructions
         pos (list 0 0)
         line #{}]
    (if (first instructions)
      (let [state (segment (list line pos) (first instructions))]
        (recur (rest instructions) (last state) (first state)))
      line)))

(defn parse-instructions [text]
  (->>
    (clojure.string/split text #",")
    (map #(list (subs % 0 1) (Integer/parseInt (subs % 1))))))

(defn max-manhattan-intersection [l1 l2]
  (->>
    (filter #(contains? l1 %) l2)
    (map #(manhattan-distance (v %) (list 0 0)))
    (apply min)))

(prn (->> "input"
  slurp 
  clojure.string/split-lines
  (map #(parse-instructions %))
  (map #(create-line %))
  (apply max-manhattan-intersection)))