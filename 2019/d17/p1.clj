(defn make-state [mem pc input output rel blocked] 
    {:mem mem :pc pc :input input :output output :rel rel :blocked blocked})
(defn init-state [mem input] (make-state mem 0 input [] 0 false))

(defn load-program [fn] 
  (as-> (slurp fn) $
    (clojure.string/split $ #",")
    (map #(bigint %) $)
    (map vector (range (count $)) $)
    (into (hash-map) $)))

(defn op-code [state] (mod ((:mem state) (:pc state)) 100))
(defn nth-digit [x n] (mod (int (/ x (Math/pow 10 n))) 10))
(defn paw [state n] ; params for writes n = nth param
  (let [mem (:mem state)
        pc (:pc state)]
    (case (nth-digit (mem pc) (+ n 1))
      0 (mem (+ n pc) 0)
      1 (mem (+ n pc) 0)
      2 (+ (:rel state) (mem (+ n pc)) 0))))

(defn par [state n] ; params for reads, n = nth param
  (let [mem (:mem state)
        pc (:pc state)]
    (case (nth-digit (mem pc) (+ n 1))
      0 (mem (mem (+ n pc)) 0)
      1 (mem (+ n pc) 0)
      2 (mem (+ (:rel state) (mem (+ n pc)) 0)))))

(defn add [state]
  (into state {
    :mem (assoc (:mem state) (paw state 3) (+ (par state 1) (par state 2)))
    :pc (+ 4 (:pc state))}))

(defn mul [state]
  (into state {
    :mem (assoc (:mem state) (paw state 3) (* (par state 1) (par state 2)))
    :pc (+ 4 (:pc state))}))

(defn inp [state]
  (if (empty? (:input state))
    (into state { :blocked true })
    (into state {
      :mem (assoc (:mem state) (paw state 1) (first (:input state)))
      :pc (+ 2 (:pc state)) 
      :input (rest (:input state))})))

(defn otp [state]
  ; (prn (par state 1))
  (into state {
    :pc (+ 2 (:pc state)) 
    :output (conj (:output state) (par state 1))}))

(defn jmp-true [state]
  (if (not= 0 (par state 1)) 
    (into state { :pc (par state 2) })
    (into state { :pc (+ (:pc state) 3) })))

(defn jmp-false [state]
  (if (= 0 (par state 1)) 
    (into state { :pc (par state 2) })
    (into state { :pc (+ (:pc state) 3) })))

(defn lt [state]
  (into state {
    :mem (assoc (:mem state) (paw state 3) (if (< (par state 1) (par state 2)) 1 0)) 
    :pc (+ (:pc state) 4)}))

(defn eq [state]
  (into state {
    :mem (assoc (:mem state) (paw state 3) (if (= (par state 1) (par state 2)) 1 0)) 
    :pc (+ (:pc state) 4)}))

(defn rel [state] 
  (into state {
    :pc (+ 2 (:pc state)) 
    :rel (+ (:rel state) (par state 1))}))

(defn halt [state] (into state {:pc -1}))
(defn halted? [state] (= (:pc state) -1))
(def OP-MAP {1 add 2 mul 3 inp 4 otp 5 jmp-true 6 jmp-false 7 lt 8 eq 9 rel 99 halt})
(defn step [state] ((OP-MAP (op-code state)) state))

(defn run [state]
  (loop [state state]
    (if (or (:blocked state) (halted? state)) 
      state
      (recur (step state)))))

;; ----- GENERIC INTCODE ABOVE -----

(defn print-grid [grid]
  (let [{width :w height :h data :data} grid]
    (doseq [y (range 0 height)] ; bounds discovered via trial and error
      (doseq [x (range 0 width)]
        (when (not= 10N (data [x y]))
          (print (str (char (data [x y] 40))))))
      (println))
    (println)))

(defn get-neighbors [pos]
  (let [[x y] pos]
    #{[(+ x 1) y] [(- x 1) y] [x (+ y 1)] [x (- y 1)]}))

; get the x,y coords for the ith member in a grid
(defn i2xy [i width] [(mod i width) (quot i width)])

(defn grid-from-stream [s]
  (let [width (+ 1 (first (filter #(= 10 (nth s %)) (range (count s)))))
        height (quot (count s) width)]
    (loop [i 0
           s s
           data {}]
      (if (empty? s)
        {:w width :h height :data data}
        (recur (inc i) (rest s) (into data {(i2xy i width) (first s)}) )))))

(defn get-grid [code]
  (grid-from-stream ((run (init-state code '())) :output)))

(defn find-intersections [grid]
  (let [{width :w height :h data :data} grid]
    (filter identity 
      (apply concat
        (for [y (range height)]
          (for [x (range width)]
            (when (= 4 (count (filter #(= 35 (data %)) (get-neighbors [x y]))))
              [x y])))))))
    
(defn sum-alignment-params [aps] 
  (reduce + (map #(* (% 0) (% 1)) aps)))

; Done by hand. Boo.
(def MAIN-ROUTINE '(\A \C \A \B \A \C \B \C \B \C))
(def A '(\R \8 \L \5 \5 \L \6 \6 \R \4))
(def B '(\R \8 \L \5 \5 \R \8))
(def C '(\R \8 \L \6 \6 \R \4 \R \4))
(def VIDEO? '(\y)) ; score doesn't print without live video. Bug in AoC?
(defn seq-to-ascii [s] (conj (mapv int (interpose \, s)) 10))
(def INPUT-FOR-PATH (apply concat (map seq-to-ascii [MAIN-ROUTINE A B C VIDEO?])))

; part1
(as-> (load-program "input") $
  (get-grid $)
  (find-intersections $)
  (sum-alignment-params $)
  (println "Part 1: " $))

; part 2
(as-> (load-program "input") $
  (init-state $ INPUT-FOR-PATH)
  (run $)
  (println "Part 2: " (last ($ :output))))

