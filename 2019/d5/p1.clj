(defn make-state [mem pc buffer] {:mem mem :pc pc :buffer buffer})

(defn op-code [y] (mod y 100))
(defn param [state n]
  (let [mem (:mem state)
        pc (:pc state)
        ins (get mem pc)]
    (if (= (mod (int (/ ins (* 10 (Math/pow 10 n)))) 10) 1)
      (get mem (+ n pc)) 
      (get mem (get mem (+ n pc))))))

(defn add [state]
  (let [mem (:mem state)
        pc (:pc state)
        buffer (:buffer state)]
    (make-state (assoc mem (get mem (+ pc 3)) (+ (param state 1) (param state 2))) 
                (+ pc 4)
                buffer)))

(defn mul [state]
  (let [mem (:mem state)
        pc (:pc state)
        buffer (:buffer state)]
    (make-state (assoc mem (get mem (+ pc 3)) (* (param state 1) (param state 2))) 
                (+ pc 4)
                buffer)))

(defn input [state]
  (let [mem (:mem state)
        pc (:pc state)
        buffer (:buffer state)]
    (make-state (assoc mem (get mem (+ pc 1)) (first buffer))
                (+ 2 pc) 
                (rest buffer))))

(defn output [state]
  (let [mem (:mem state)
        pc (:pc state)
        buffer (:buffer state)
        ins (get mem pc)]
    (prn (param state 1))
    (make-state mem (+ 2 pc) buffer)))

(defn jmp-true [state]
  (let [mem (:mem state)
        pc (:pc state)
        buffer (:buffer state)
        a (param state 1)
        b (param state 2)]
    (if (not= a 0)
      (make-state mem b buffer)
      (make-state mem (+ 3 pc) buffer))))

(defn jmp-false [state]
  (let [mem (:mem state)
        pc (:pc state)
        buffer (:buffer state)
        a (param state 1)
        b (param state 2)]
    (if (= 0 a) 
      (make-state mem b buffer)
      (make-state mem (+ 3 pc) buffer))))

(defn lt [state]
  (let [mem (:mem state)
        pc (:pc state)
        buffer (:buffer state)
        a (param state 1)
        b (param state 2)]
    (make-state (assoc mem (get mem (+ pc 3)) (if (< a b) 1 0)) 
                (+ pc 4) 
                buffer)))

(defn eq [state]
  (let [mem (:mem state)
        pc (:pc state)
        buffer (:buffer state)
        a (param state 1)
        b (param state 2)]
    (make-state (assoc mem (get mem (+ pc 3)) (if (= a b) 1 0)) 
                (+ pc 4) 
                buffer)))

(defn step [state]
  (let [mem (:mem state)
        pc (:pc state)
        op (op-code (get mem pc))]
    (case op
      1 (add state)
      2 (mul state)
      3 (input state)
      4 (output state)
      5 (jmp-true state)
      6 (jmp-false state)
      7 (lt state)
      8 (eq state)
      99 (make-state mem -1 "") ; Halt
      :else (throw (Exception. "invalid op code")))))

(defn run [mem pc buffer]
  (loop [state (make-state mem pc buffer)]
    (if (= (:pc state) -1)
      (:mem state)
      (recur (step state)))))

(defn load-program [fn] 
  (vec (map #(Integer/parseInt %) (clojure.string/split (slurp fn) #","))))

; part 1
(run (load-program "input") 0 (list 1))

; part 2
(run (load-program "input") 0 (list 5))