;; state = [mem pc input-input]
;; buiffer is a list of ints
(defn make-state [mem pc input output rel] 
    {:mem mem :pc pc :input input :output output :rel rel})
(defn update-state [state delta] (into state delta))
(defn init-state [mem input] (make-state mem 0 input [] 0))

(defn op-code [state] (mod ((:mem state) (:pc state)) 100))
(defn nth-digit [x n] (mod (int (/ x (Math/pow 10 n))) 10))
(defn paw [state n] ; params for writes n = nth param
  (let [mem (:mem state)
        pc (:pc state)]
    (case (nth-digit (get mem pc) (+ n 1))
      0 (get mem (+ n pc) 0)
      1 (get mem (+ n pc) 0)
      2 (+ (:rel state) (get mem (+ n pc)) 0))))

(defn par [state n] ; params for reads, n = nth param
  (let [mem (:mem state)
        pc (:pc state)]
    (case (nth-digit (get mem pc) (+ n 1))
      0 (get mem (get mem (+ n pc)) 0)
      1 (get mem (+ n pc) 0)
      2 (get mem (+ (:rel state) (get mem (+ n pc)) 0)))))

(defn add [state]
  (update-state state {
    :mem (assoc (:mem state) (paw state 3) (+ (par state 1) (par state 2)))
    :pc (+ 4 (:pc state))}))

(defn mul [state]
  (update-state state {
    :mem (assoc (:mem state) (paw state 3) (* (par state 1) (par state 2)))
    :pc (+ 4 (:pc state))}))

(defn inp [state]
  (update-state state {
    :mem (assoc (:mem state) (paw state 1) (first (:input state)))
    :pc (+ 2 (:pc state)) 
    :input (rest (:input state))}))

(defn otp [state]
  (prn (par state 1))
  (update-state state {
    :pc (+ 2 (:pc state)) 
    :output (conj (:output state) (par state 1))}))

(defn jmp-true [state]
  (if (not= 0 (par state 1)) 
    (update-state state { :pc (par state 2) })
    (update-state state { :pc (+ (:pc state) 3) })))

(defn jmp-false [state]
  (if (= 0 (par state 1)) 
    (update-state state { :pc (par state 2) })
    (update-state state { :pc (+ (:pc state) 3) })))

(defn lt [state]
  (update-state state {
    :mem (assoc (:mem state) (paw state 3) (if (< (par state 1) (par state 2)) 1 0)) 
    :pc (+ (:pc state) 4)}))

(defn eq [state]
  (update-state state {
    :mem (assoc (:mem state) (paw state 3) (if (= (par state 1) (par state 2)) 1 0)) 
    :pc (+ (:pc state) 4)}))

(defn rel [state]
  (update-state state {
    :pc (+ 2 (:pc state))
    :rel (+ (:rel state) (par state 1))}))

(defn halt [state] (update-state state {:pc -1}))
(defn halted? [state] (= (:pc state) -1))

(def OP-MAP {1 add 2 mul 3 inp 4 otp 5 jmp-true 6 jmp-false 7 lt 8 eq 9 rel 99 halt})
(defn step [state] ((OP-MAP (op-code state)) state))

(defn run [mem input]
  (loop [state (init-state mem input)]
    (if (halted? state)
      state
      (recur (step state)))))

(defn load-program [fn] 
  (as-> (slurp fn) $
    (clojure.string/split $ #",")
    (map #(bigint %) $)
    (map vector (range (count $)) $)
    (into (hash-map) $)))

(run (load-program "input") '(1))
(run (load-program "input") '(2))