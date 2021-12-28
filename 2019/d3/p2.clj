;; state = (line, points, current-position)
;; current-position = (x y)
;; points = all points in line, [(x1 y1) (x2 y2) ...]
;; instruction = (direction distance)

(defn k [x y] (str x "," y))
(defn v [k] 
  (let [x (Integer/parseInt (first (clojure.string/split k #",")))
        y (Integer/parseInt (last (clojure.string/split k #",")))]
  (list x y)))

(defn move [state dx dy n]
  (loop [line (first state)
         points (second state)
         pos (last state)
         n n]
    (if (= n 0)
        (list line points pos)
        (recur (conj line (k (+ dx (first pos)) (+ dy (last pos))))
               (conj points (k (+ dx (first pos)) (+ dy (last pos))))
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

(defn create-line [instructions]
  (loop [instructions instructions
         line []
         points #{}
         pos (list 0 0)]
    (if (first instructions)
      (let [state (segment (list line points pos) (first instructions))]
        (recur (rest instructions) (first state) (second state) (last state)))
      (list line points))))

(defn parse-instructions [text]
  (->>
    (clojure.string/split text #",")
    (map #(list (subs % 0 1) (Integer/parseInt (subs % 1))))))

(defn nearest-intersection [l1 l2]
    (let [intersections (filter #(contains? (last l1) %) (last l2))]
        (apply min 
            (map #(+ (.indexOf (first l1) %) (.indexOf (first l2) %)) intersections))))

(prn (->> "input"
  slurp 
  clojure.string/split-lines
  (map #(parse-instructions %))
  (map #(create-line %))
  (apply nearest-intersection)
  (+ 2)))