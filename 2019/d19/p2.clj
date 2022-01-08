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
      2 (+ (:rel state) (mem (+ n pc))))))

(defn par [state n] ; params for reads, n = nth param
  (let [mem (:mem state)
        pc (:pc state)]
    (case (nth-digit (mem pc) (+ n 1))
      0 (mem (mem (+ n pc)) 0)
      1 (mem (+ n pc) 0)
      2 (mem (+ (:rel state) (mem (+ n pc)) 0) 0))))

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


(def CODE (load-program "input"))

(defn tract-for-coord [x y]
  (first ((run (init-state CODE [x y])) :output)))

(defn find-square [size]
  (loop [x 5 y 7]
    (let [cur (tract-for-coord x y)
          opp (tract-for-coord (+ x (- size 1)) (- y (- size 1)))]
      (cond 
        (= 1 cur opp) [x (- y (- size 1))]
        (= 1 cur) (recur x (inc y))
        :else (recur (inc x) y)))))

(prn (find-square 100)) 