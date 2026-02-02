# The Evolution of LLM Agents: A Technical Analysis of LLM-Driven Architectures (2022–2025)

## 1. Introduction: The Agentic Shift in Artificial Intelligence

- The trajectory of Large Language Models (LLMs) has undergone a profound metamorphosis between 2022 and 2025. 
- What began as a revolution in static text generation and zero-shot generalization has evolved into the paradigm of "Agentic AI"-systems capable of perception, reasoning, planning, and autonomous execution within dynamic environments. 
- This transition marks a fundamental departure from the passive "prompt-response" interaction model toward architectures that exhibit goal-directed behavior, persistency, and self-correction. 
- The shift is not merely functional but architectural; it represents a move from the LLM as a solitary oracle to the LLM as a central cognitive engine (or "brain") within a larger, modular computational system.
- The development of LLM-driven agents has not been linear but rather punctuated by specific architectural milestones that solved critical bottlenecks in reliability, context management, and reasoning depth. 

- Initial efforts focused on breaking the linearity of chain-of-thought prompting, leading to iterative frameworks like ReAct that coupled reasoning with external tools. 
- As the limitations of single-turn reasoning became apparent, the field moved toward cognitive architectures incorporating explicit memory streams, reflection mechanisms, and tree-based search algorithms such as Tree of Thoughts (ToT). 
- The years 2024 and 2025 have witnessed the crystallization of "System 2" thinking in agents-characterized by deliberation, search-time compute scaling, and multi-agent orchestration-culminating in generalist systems like Magentic-One and reasoning heavyweights like rStar-Math.
- This report provides an exhaustive technical analysis of these milestones. It deconstructs the seminal papers that defined this era, isolating the mathematical formulations, algorithmic innovations, and structural designs that have enabled LLMs to transcend language modeling and achieve genuine agency. By tracing the lineage from simple "reasoning-acting" loops to complex, self-evolving multi-agent ecosystems, we illuminate the underlying mechanisms driving the current explosion in autonomous system capabilities.

## 2. Breaking Linearity: The Synergy of Reasoning and Acting (2022–2023)

- The initial phase of agentic architecture focused on coupling the internal reasoning capabilities of LLMs with external action spaces.

- Prior to late 2022, models were largely trapped in "internal hallucinations," unable to verify facts or interact with the world. - The introduction of ReAct marked the first major architectural shift toward grounding LLMs in external reality, fundamentally altering how prompts were structured and how models were expected to behave.

### 2.1 ReAct: Synergizing Reasoning and Acting in Language Models

**Paper Title: ReAct: Synergizing Reasoning and Acting in Language Models (2022)**

**Paper Link:** [https://arxiv.org/abs/2210.03629]

#### Summary and Architectural Context

- Before the advent of ReAct, the landscape of LLM capabilities was bifurcated into two distinct paradigms: Chain-of-Thought (CoT) prompting and Action-only generation. 
- CoT demonstrated that LLMs could perform complex reasoning by generating intermediate steps, but it remained disconnected from the external world, leading to error propagation and hallucination.
- Conversely, Action-only models could interact with environments (e.g., text games or web APIs) but lacked the high-level planning and reasoning capabilities to handle long-horizon tasks or exceptions.
- Yao et al. (2022) introduced ReAct, a general paradigm that prompts LLMs to generate both reasoning traces and task-specific actions in an interleaved manner.
    - This synergy allows the model to induce, track, and update action plans while handling exceptions through reasoning ("Reason to Act"), and simultaneously interface with external sources (like Wikipedia APIs) to gather information ("Act to Reason").
    - The ReAct framework essentially provided the LLM with a "working memory" of its own thought process alongside the observation history of the world, creating a feedback loop that was notably absent in previous architectures.

#### Key Findings

- The authors demonstrated that interleaving reasoning and action outperforms purely reasoning-based or action-based baselines across diverse benchmarks.
- Knowledge-Intensive Tasks: On HotpotQA and FEVER, ReAct overcame the prevalent issues of hallucination in CoT. By interacting with a Wikipedia API, the model could verify its internal knowledge against external facts, generating human-like task-solving trajectories that were more interpretable and trustworthy.
- Decision-Making Tasks: On the ALFWorld benchmark, ReAct outperformed imitation learning methods by significant margins (an absolute success rate improvement of 34%) and reinforcement learning baselines, despite utilizing only one or two in-context examples.
- Interpretability: The interleaved traces provided a transparent log of the model's decision-making process, allowing human observers to diagnose exactly where a plan failed-whether in the reasoning step (logic error) or the action step (execution error).

#### Mathematical Formulation: The Augmented Action Space

- The ReAct framework formalizes the agent's interaction as a sequential decision-making process where the action space is fundamentally expanded.
- Let the standard action space be $A$, denoting the set of external environment actions (e.g., search[query], click[link], lookup[term]). 
- ReAct augments this with a language space $L$, representing "thoughts" or reasoning traces. The total action space becomes $\hat{A} = A \cup L$.
- At any time step $t$, the agent observes a context $c_t$, which is a sequence of prior observations and actions:
$$c_t = (o_1, a_1, \dots, o_{t-1}, a_{t-1}, o_t)$$

- The policy $\pi$, parameterized by the LLM, generates an action $\hat{a}_t \in \hat{A}$ based on this context:

$$\hat{a}_t \sim \pi(\cdot \mid c_t)$$

- The critical innovation lies in how the context updates depending on the type of action selected:
    - Reasoning Step (Thought): If $\hat{a}_t \in L$, the action is a thought (e.g., "I need to search for the director of the movie"). This action does not affect the external environment state. However, it updates the context for the next step, providing semantic guidance for future actions. This represents the "Reason to Act" pathway:
        $$c_{t+1} = (c_t, \hat{a}_t)$$
    - Action Step (Execution): If $\hat{a}_t \in A$, the action is an external command (e.g., search). The environment executes this action and returns a new observation $o_{t+1}$ (e.g., "The Wachowskis"). The context is updated with both the action and the observation. This represents the "Act to Reason" pathway.:
        $$c_{t+1} = (c_t, \hat{a}_t, o_{t+1})$$


- This formulation allows the trajectory $\tau$ to consist of flexible sequences like $(Thought, Thought, Action, Observation, Thought, \dots)$. 
- In contrast to standard Reinforcement Learning (RL) where observations are immediate consequences of actions, ReAct treats thoughts as actions that modify the internal state (context) without modifying the external state, bridging the gap between cognitive processing and embodied action.

### 2.2 Toolformer: Self-Supervised Tool Learning

**Paper Title: Toolformer: Language Models Can Teach Themselves to Use Tools (2023)**

**Paper Link:** [https://arxiv.org/abs/2302.04761]

#### Summary and Architectural Context

- While ReAct relied on few-shot prompting (in-context learning) to induce tool use, this approach had limitations: it consumed valuable context window space and relied heavily on the quality of the provided examples. 

- Toolformer, introduced by Schick et al. (2023), proposed a method for LLMs to learn tool usage parameters implicitly during training, without the need for massive human annotation.

- The paper introduces a self-supervised process where the model annotates a raw text dataset with potential API calls, executes them, and filters them based on a rigorous loss-based criterion. This marked a shift from "prompted agents" to "tuned agents" that possess inherent tool-using capabilities.

#### Key Findings

- Toolformer demonstrated that a relatively small model (6.7B parameter GPT-J) could outperform the much larger GPT-3 (175B) on tasks requiring factual lookup, precise calculation, and translation.

- Crucially, the model learned to use tools continuously and autonomously, deciding when to call an API and what arguments to pass, solely based on the learned utility of the tool in predicting subsequent text. This eliminated the need for specific trigger words or rigid prompt structures during inference.

#### Mathematical Formulation: The Loss-Based Filtering Criterion

- The core technical contribution of Toolformer is the mathematical formulation used to determine if an API call is genuinely helpful. The goal is to generate a dataset $C^*$ augmented with API calls from a raw dataset $C$.

- Let $x = x_1, \dots, x_n$ be a sequence of tokens. The model samples a position $i$ and generates a candidate API call $c_i$ (e.g., Calc(1+1)) which yields a result $r_i$ (e.g., 2).
To evaluate the utility of this call, the authors define a weighted cross-entropy loss $L_i(z)$ for predicting tokens $x_i, \dots, x_n$ given a prefix $z$. The weights $w_{j-i}$ are designed to decay as the distance from the API call increases, focusing the evaluation on the immediate context (since tool use typically helps predict the tokens immediately following it):
$$L_i(z) = - \sum_{j=i}^n w_{j-i} \cdot \log p_M(x_j \mid z, x_{1:j-1})$$

- The filtering mechanism compares two specific loss values:
Loss with Tool ($L^+$): The loss when the API call $c_i$ and its response $r_i$ are inserted into the sequence.
$$L^+_i = L_i(e(c_i, r_i))$$
where $e(c_i, r_i)$ represents the sequence containing the API call and the result token → and </API>.

- Loss without Tool ($L^-$): The baseline loss. This is defined as the minimum of two scenarios: performing no API call ($\epsilon$) or performing the call but receiving no result (to ensure the model isn't just memorizing the call itself).
$$L^-_i = \min(L_i(\epsilon), L_i(e(c_i, \epsilon)))$$

- The candidate API call is considered useful-and thus retained in the fine-tuning dataset-only if the reduction in loss exceeds a filtering threshold $\tau_f$:
$$L^-_i - L^+_i \ge \tau_f$$

- This inequality ensures that the model only learns tool behaviors that provide significant informational gain for predicting the subsequent text. By fine-tuning on datasets constructed via this logic, Toolformer internalizes the "knowledge" of tools, treating API calls as just another form of language generation that minimizes entropy.

## The Loop of Improvement: Self-Correction and Cognitive Architectures (2023)

- By 2023, the limitations of simple linear execution-even when augmented with tools-became evident. Agents attempting complex, multi-step tasks often failed due to error propagation; a single mistake in step 3 would derail the entire trajectory. To address this, researchers began looking at "cognitive architectures" that mimicked human learning loops, specifically the ability to reflect on past actions and persist memory over time.

### 3.1 Reflexion: Verbal Reinforcement Learning

**Paper Title: Reflexion: Language Agents with Verbal Reinforcement Learning (2023)**

**Paper Link:** [https://arxiv.org/abs/2303.11366]

#### Summary and Architectural Context

- Traditional Reinforcement Learning (RL) optimizes agents by updating numerical weights based on scalar reward signals. 
- However, applying RL to LLMs (e.g., PPO) is computationally expensive and difficult to tune for complex reasoning tasks where a binary "success/fail" signal offers little guidance on why a failure occurred. 
- Shinn et al. (2023) introduced Reflexion, a framework that substitutes traditional weight updates with linguistic feedback.9 In this paradigm, the agent receives a verbal critique of its failure, reflects on this critique to generate a textual "lesson," and stores this lesson in an episodic memory buffer to condition future attempts. 
- This effectively allows the agent to "debug" its own reasoning.

#### Key Findings

- Reflexion achieved state-of-the-art results on diverse and challenging benchmarks.
- Coding: On the HumanEval benchmark, Reflexion achieved a 91% pass@1 accuracy, significantly surpassing the base GPT-4 performance of 80%.10
- Sequential Decision Making: On ALFWorld, it demonstrated the ability to recover from repetitive failure loops (e.g., repeatedly trying to open a locked door) by self-reflecting and changing strategy, outperforming ReAct baselines.
- Efficiency: The method demonstrated that "verbal RL" could achieve improvements comparable to fine-tuning but with a fraction of the compute, as the "parameters" being updated are simply the text in the context window.

#### Mathematical Formulation and Algorithm: The Semantic Gradient

- The Reflexion framework is defined by a tuple of three distinct models: the Actor ($M_a$), the Evaluator ($M_e$), and the Self-Reflection ($M_{sr}$).
- The agent's policy is parameterized not just by the LLM weights $\theta$, but also by its memory encoding $mem$. The policy is denoted as $\pi_\theta(a_t \mid s_t, mem)$.
- The Reflexion Loop proceeds as follows:
    - Initialization: The memory buffer is initialized $mem = \emptyset$.
    - Trial Generation ($k=0$): The Actor interacts with the environment to produce a trajectory $\tau_0$.
    - Evaluation: The Evaluator scores the trajectory to produce a scalar reward $r_0 = M_e(\tau_0)$. If $r_0$ indicates success, the loop terminates.
    - Reflection (The "Update"): If the task fails, the Self-Reflection model analyzes the trajectory $\tau_0$ and the error signal to produce a specific verbal summary or critique $sr_0$: $$sr_0 = M_{sr}(\tau_0, r_0)$$

- This $sr_0$ acts as a "semantic gradient" - a directional vector in language space indicating how to improve.
- Memory Optimization: The summary is appended to the memory buffer:
        $$mem \leftarrow mem \cup \{sr_0\}$$

- Crucially, the memory is often constrained to a sliding window of the last $\Omega$ reflections to fit within context limits.
- Next Trial ($k+1$): The Actor generates a new trajectory $\tau_{k+1}$, but this time the policy is conditioned on the updated memory:
    $$a_{t+1} \sim \pi_\theta(\cdot \mid s_{t+1}, mem)$$
- This conditioning allows the agent to explicitly reason about its past mistakes (e.g., "I previously failed because I didn't check the inventory; this time I will check the inventory first"). Mathematically, this approximates policy gradient methods where the "gradient" is explicated in natural language rather than computed via backpropagation.

### Generative Agents: Interactive Simulacra of Human Behavior

**Paper Title: Generative Agents: Interactive Simulacra of Human Behavior (2023)**

**Paper Link:** [https://arxiv.org/abs/2304.03442]

#### Summary and Architectural Context

- While Reflexion focused on task-solving loops, Park et al. (2023) focused on long-term consistency and social believability. 
- Their paper on Generative Agents proposed a comprehensive architecture for creating agents that inhabit a sandbox environment (Smallville) and interact over simulated days and weeks. 
- The core contribution was a persistent memory architecture comprising a memory stream, a retrieval mechanism, and recursive reflection and planning modules.13

#### Key Findings

- The architecture enabled emergent social behaviors that were not explicitly programmed. For instance, an agent initiated a Valentine's Day party, and the news autonomously spread through the village via agent-to-agent dialogue. 
- Agents remembered past interactions, coordinated schedules, and formed relationships, demonstrating that LLMs could maintain coherent identities over long time horizons if supported by the right memory architecture.

#### Mathematical Formulation: The Retrieval Score

- The memory stream is a comprehensive list of all agent experiences. 
- To function within limited context windows, a retrieval function is required to select only the most relevant memories for the current moment. 
- The relevance of a memory $m$ to a current query context $q$ is calculated via a weighted sum of three distinct components:
    $$Score(m, q) = \alpha \cdot R(m) + \beta \cdot I(m) + \gamma \cdot S(m, q)$$
- Recency $R(m)$: An exponential decay function assigns higher scores to memories that were accessed recently, ensuring the agent remains responsive to the immediate present.
    $$R(m) = e^{-\lambda \Delta t}$$
    where $\Delta t$ is the number of time steps since the last access.
- Importance $I(m)$: A scalar score (e.g., 1-10) generated by the LLM at the time of memory creation. This distinguishes mundane events (e.g., "eating breakfast") from significant ones (e.g., "getting a promotion").
- Relevance $S(m, q)$: The semantic similarity between the memory and the current situation, calculated using the cosine similarity of their embedding vectors:
    $$S(m, q) = \frac{\vec{v}_m \cdot \vec{v}_q}{\|\vec{v}_m\| \|\vec{v}_q\|}$$
- The parameters $\alpha, \beta, \gamma$ are weights that balance these factors. This scoring function allows the agent to retrieve information that is timely, significant, and contextually appropriate, forming the basis of "believable" agent behavior.14

## Structured Reasoning: Trees and Graphs (2023–2024)

- As tasks grew in complexity, linear Chain-of-Thought reasoning proved insufficient for problems requiring lookahead, backtracking, or combining multiple streams of information. 
- This necessitated architectures that structured reasoning into non-linear topologies, treating thought processes as search problems over data structures.

### 4.1 Tree of Thoughts (ToT): Deliberate Problem Solving

**Paper Title: Tree of Thoughts: Deliberate Problem Solving with Large Language Models (2023)**

**Paper Link:** [https://arxiv.org/abs/2305.10601]

#### Summary and Architectural Context

- Chain-of-Thought (CoT) prompting relies on the greedy decoding of tokens, which mimics "System 1" (fast, intuitive) thinking. 
- However, complex problems like mathematical puzzles or creative writing often require "System 2" (slow, deliberate) thinking-exploring multiple possibilities, evaluating them, and backtracking if necessary. Yao et al. (2023) introduced Tree of Thoughts (ToT), a framework that generalizes CoT by allowing the model to maintain a tree of partial solutions.

#### Key Findings

- The effectiveness of ToT was demonstrated on the "Game of 24" (a math puzzle). 
- While standard CoT achieved only a 4% success rate, ToT achieved 74%. 
- This massive leap proved that LLMs possess latent capabilities for planning and lookahead that remain dormant under standard prompting but are activated when inference is structured as a search algorithm.

#### Mathematical Formulation: Search over Thoughts

- ToT frames problem-solving as a search over a tree where each node $s = [x, z_{1 \dots i}]$ represents a state containing the input $x$ and a sequence of thoughts $z$.
- The framework involves four components:
    - Thought Decomposition: The problem is broken down into intermediate steps $z_i$ (e.g., an intermediate equation).
    - Thought Generation $G(p_\theta, s, k)$: The model generates $k$ candidates for the next step.
    $$z^{(j)} \sim p_\theta(z_{i+1} \mid s) \quad \text{for } j=1 \dots k$$
    - State Evaluation $V(p_\theta, S)$: A crucial component where the LM explicitly evaluates the "promise" of a state $s$ to lead to a solution. This effectively acts as a heuristic function in the search. The evaluation can be a value classification (e.g., "sure", "maybe", "impossible") or a scalar score.
    - Search Algorithm:
        - BFS (Breadth-First Search): Maintains a set of the $b$ most promising states at each step, pruning the rest.
        - DFS (Depth-First Search): Explores a path until a leaf is reached or the state evaluation drops below a threshold $v_{th}$ ($V(s) \le v_{th}$), triggering backtracking to the parent node.
- This synthesis of generation and explicit evaluation allows the agent to look ahead and prune unpromising branches early, a feature entirely absent in linear CoT.

### Graph of Thoughts (GoT): Networked Reasoning

**Paper Title: Graph of Thoughts: Solving Elaborate Problems with Large Language Models (2023)**

**Paper Link:** [https://arxiv.org/abs/2308.09687]

#### Summary and Architectural Context

- Besta et al. (2023) argued that even trees are too restrictive for certain classes of problems that require combining information from divergent branches. 
- They extended ToT to Graph of Thoughts (GoT), modeling reasoning as a Directed Acyclic Graph (DAG) or even cyclic graphs.
- This allows for operations impossible in trees, such as aggregation (combining multiple independent thoughts into a stronger solution) and looping (refining a thought recursively).

#### Key Findings

- GoT outperformed ToT in tasks like sorting and document merging, where combining information from different reasoning branches is essential. 
- In sorting tasks, GoT improved quality by 62% over ToT while simultaneously reducing costs by 31%.20 The cost reduction comes from the graph's ability to "converge" multiple paths into a single solution, avoiding the redundant expansion of parallel tree branches.

#### Mathematical Formulation: The Graph Tuple

- Reasoning in GoT is modeled as a tuple $(G, T, E, R)$:
    - $G = (V, E)$: The graph where vertices $v$ are thoughts (LLM outputs) and edges $e$ are dependencies.
    - $T$: A set of Thought Transformations. Beyond the standard Generate (1-to-1), GoT introduces Aggregate ($k$-to-1), where a new thought $v_{new}$ is generated based on the information from multiple parent thoughts $v_1, \dots, v_k$:
        $$v_{new} = \text{LLM}(v_1, \dots, v_k; \text{prompt}_{agg})$$
    - $E$: An Evaluation function scoring vertices to determine their quality.
    - $R$: A Ranking function to select the most relevant thoughts for the next expansion.

- This topology enables "volume" in reasoning-utilizing the collective information of a whole layer of thoughts rather than just the history of a single path. 
- It mimics complex cognitive processes like "brainstorming" (branching) followed by "convergence" (aggregation).

## Embodied and Lifelong Learning Agents (2023–2024)

- Moving from static text benchmarks to open-ended worlds, agents required the ability to learn skills continuously and adapt to environments without re-training weights. This "in-context learning" evolution reached a peak with the Voyager system.

### Voyager: Open-Ended Embodied Agent with LLMs

**Paper Title: Voyager: An Open-Ended Embodied Agent with Large Language Models (2023)**

**Paper Link:** [https://arxiv.org/abs/2305.16291]

#### Summary and Architectural Context

- Previous embodied agents relied heavily on Reinforcement Learning (RL) which required massive training data and struggled with generalization. Wang et al. (2023) introduced Voyager, the first LLM-powered embodied lifelong learning agent in Minecraft that operates without gradient-based training.24 Voyager interacts with GPT-4 to generate executable code, treating code generation as its action space.

#### Key Findings

- Voyager achieved what was previously considered a "grand challenge" for autonomous agents: unlocking the "diamond" tech tree level in Minecraft without human intervention. 
- It demonstrated 3.3x more unique item discovery and traveled 2.3x longer distances than prior SOTA baselines. 
- Crucially, its skill library allowed for zero-shot generalization to new worlds-it could start a new game and immediately use skills learned in a previous game.

#### Architecture and Algorithms: The Automatic Curriculum

- Voyager consists of three main components that function as a continuous learning loop:
    - Automatic Curriculum: An LLM-driven module that proposes tasks based on the agent's current inventory and exploration state. Unlike standard RL which maximizes a scalar reward, the curriculum prompts GPT-4 to suggest tasks that are at the frontier of the agent's current capabilities (e.g., "You have wood, now craft a crafting table" rather than "Go fight a dragon"). This acts as an intrinsic motivation mechanism.
    - Iterative Prompting Mechanism:
        - The agent generates code (a skill function) to achieve the proposed task.
        - The code is executed in the environment via the Mineflayer API.
    - Feedback Loop: If execution fails (Java error) or the goal is not met (inventory unchanged), the error trace and environment observation are fed back to the LLM.
    - The LLM refines the code based on this feedback in a closed loop until success.
    - Skill Library (Vector Memory):
        - Once a task is successfully completed, the working code is stored in a vector database as a "skill," indexed by the embedding of its docstring description.
    - Retrieval: For new tasks, Voyager retrieves relevant skills from this library. This allows for compositional behavior: to craft_sword, the agent retrieves and executes craft_planks and craft_sticks.
- This architecture proved that executable code is a superior action space for LLM agents compared to low-level motor commands, as code naturally represents temporally extended, compositional, and abstract actions.
## The Multi-Agent Revolution and Standardized Procedures (2023–2024)

- As single-agent systems faced bottlenecks in context length and role confusion, 2023 saw the rise of Multi-Agent Systems (MAS). These frameworks distribute cognition across specialized personas, mimicking human organizational structures to handle complexity.

### MetaGPT: Meta Programming for Multi-Agent Collaboration

**Paper Title: MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework (2023)**

**Paper Link:** [https://arxiv.org/abs/2308.00352]

#### Summary and Architectural Context

- Early multi-agent attempts (like ChatDev) often devolved into unproductive "chatter" or hallucination spirals where agents reinforced each other's errors. Hong et al. (2023) addressed this by introducing MetaGPT, a framework rooted in the philosophy that "Code = SOP(Team)". 
- This implies that high-quality software output is the result of encoding Standard Operating Procedures (SOPs) into the agent team structure, rather than leaving interaction protocols open-ended.

#### Key Findings

- MetaGPT achieved State-of-the-Art (SOTA) on the HumanEval (85.9%) and MBPP (87.7%) benchmarks for code generation.30 It successfully simulated a software company (Product Manager, Architect, Engineer, QA) to generate a complete software project-including data structures, APIs, and documentation-from a single one-line prompt.

#### Algorithmic Structure: Role-Based Watch Mechanism

- MetaGPT formalizes collaboration through a Publish-Subscribe mechanism rather than direct dialogue.
- Role Definition: Each agent $A_i$ (e.g., Architect) is initialized with a specific profile and a _watch list. The agent "watches" for specific message types in the shared environment.
    $$\text{Observation}_i = \text{Environment}.\text{peek}(\text{Trigger}_i)$$
- Action Execution: Upon observing a relevant trigger (e.g., a "Product Requirement Document" appearing in the environment), the agent performs a specialized action (e.g., "Write Design Document").
    $$\text{Output}_i = \text{Action}_i(\text{Observation}_i)$$
- Publication: The output is published back to the shared environment, serving as the trigger for downstream agents (e.g., the Engineer watches for the Design Document).
- The SOP is essentially a directed acyclic graph (DAG) of these triggers and actions. This constrains the search space of interactions, preventing the "infinite loop" common in unstructured chats and ensuring a waterfall-like progression of task completion.

### AgentVerse: Facilitating Multi-Agent Collaboration

**Paper Title: AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors in Agents (2023)**

**Paper Link:** [https://arxiv.org/abs/2308.10848]

#### Summary and Key Findings

- While MetaGPT focused on rigid SOPs, AgentVerse explored dynamic agent recruitment and diverse collaboration structures.34 Chen et al. proposed a framework where the system dynamically recruits expert agents based on the problem description.

#### Key Algorithm
- The framework splits problem-solving into four stages:
    - Expert Recruitment: Selecting agents best suited for the task.
    - Collaborative Decision Making: Agents discuss using either Horizontal (all agents discuss together) or Vertical (hierarchical) communication structures.
    - Action Execution: Agents act in the environment.
    - Evaluation: The state is scored, and feedback loops back to the decision stage.
- This flexibility allowed AgentVerse to outperform single agents in reasoning and coding tasks by leveraging the "wisdom of the crowd" and emergent behaviors like one agent voluntarily correcting another.

## System 2 Reasoning and Search-Based Scaling (2024–2025)

- The most significant development in the 2024-2025 period is the formalization of "System 2" reasoning in agents. Inspired by Kahneman’s distinction between fast, intuitive thinking (System 1) and slow, deliberate thinking (System 2), researchers began focusing on inference-time search and rigorous verification to scale intelligence.

### Agent Q: Combining MCTS and DPO

**Paper Title: Agent Q: Advanced Reasoning and Learning for Autonomous AI Agents (2024)**

**Paper Link:** [https://arxiv.org/abs/2408.07199]

#### Summary and Architectural Context

- Standard supervised fine-tuning (SFT) on expert demonstrations often fails to generalize to complex, dynamic web environments. 
- Putta et al. (2024) introduced Agent Q, a framework that bridges the gap between static pre-training and dynamic agentic decision-making by combining Guided Monte Carlo Tree Search (MCTS) with an off-policy version of Direct Preference Optimization (DPO).37

#### Key Findings

- Agent Q boosted Llama-3 70B's zero-shot success rate on real-world booking scenarios from 18.6% to 81.7% after just one day of autonomous data collection, eventually reaching 95.4% with online search capabilities. 
- This proved that agents could self-improve by learning from their own successes and failures.

#### Mathematical Formulation: DPO on Search Trees

- The innovation lies in using MCTS to generate the preference data for DPO.
- MCTS Exploration: The agent builds a search tree where nodes are web states and edges are actions (clicks, types).
- Soft-Q Evaluation: A heuristic function estimates the value of leaf nodes (success probability).
- Contrastive Pair Creation: Divergent branches in the tree that lead to different outcomes form the preference pairs $(y_w, y_l)$, where $y_w$ is a winning trajectory and $y_l$ is a losing one.
- The DPO loss function is adapted to optimize the policy $\pi_\theta$ using these self-generated pairs:

$$\mathcal{L}_{DPO}(\pi_\theta; \pi_{ref}) = - \mathbb{E}_{(x, y_w, y_l) \sim D} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{ref}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{ref}(y_l \mid x)} \right) \right]$$

- By optimizing this objective, the model internalizes the "planning" capability of MCTS into its weights, effectively distilling the search process into its base "System 1" intuition.

### rStar-Math: Self-Evolved Deep Thinking

**Paper Title: rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking (2025)**

**Paper Link:** [https://arxiv.org/abs/2501.04519]

#### Summary and Architectural Context

- Guan et al. (2025) challenged the dominance of massive proprietary models (like OpenAI o1) by demonstrating that small language models (SLMs) could achieve frontier-level math reasoning through "deep thinking". 
- rStar-Math employs a self-evolutionary process using MCTS and a novel Process Preference Model (PPM).

#### Key Findings

- rStar-Math improved a 7B model (Qwen2.5-Math) from 58.8% to 90.0% on the MATH benchmark, surpassing even o1-preview. This demonstrated that the reasoning gap between small and large models could be bridged by test-time compute.

#### Algorithmic Innovation: MCTS Self-Evolution

- The core mechanism is a 4-round iterative evolution loop:
    - Code-Augmented Data Synthesis: The model explores solution paths using MCTS. Uniquely, each node generates a reasoning step and Python code. Only nodes where the code executes successfully are retained, filtering out hallucinated logic.
    - Q-Value Annotation: Nodes are not scored by a static reward model but by their statistical contribution to correct answers across thousands of rollouts. A step $s$ receives a high Q-value if it appears frequently in successful trajectories.
    - PPM Training: A reward model is trained to predict these Q-values using a pairwise ranking loss. This PPM then guides the MCTS in the next round. 
    $$\mathcal{L}_{PPM} = - \log \sigma(r(s_{pos}) - r(s_{neg}))$$
    where $s_{pos}$ is a step with a higher Q-value than $s_{neg}$.
    - This creates a positive feedback loop: better search generates better data, which trains a better reward model, which guides a better search.

### LIMO: Less is More for Reasoning

**Paper Title: LIMO: Less is More for Reasoning (2025)**

**Paper Link:** [https://arxiv.org/abs/2502.03387]

#### Summary and Key Findings

- In a counter-narrative to the "scaling laws" that demand massive datasets, the LIMO paper (2025) posits the "Less-Is-More Reasoning Hypothesis." 
- The authors demonstrate that complex reasoning capabilities can be elicited using only 817 carefully curated training samples.
Key Result: LIMO achieved 57.1% on the AIME benchmark (up from 6.5% with standard fine-tuning), outperforming models trained on datasets 100x larger.
- Implication: This suggests that reasoning in LLMs is not learned from scratch during fine-tuning but is largely pre-encoded during pre-training. 
- The fine-tuning phase merely requires high-quality "cognitive templates" that explicate the process of reasoning (e.g., "I need to check this assumption") rather than just the answer. 
- This shifts the focus of agent training from data quantity to data structure.

## Generalist Systems and Orchestration (2024–2025)

- The convergence of memory, tools, and multi-agent planning has led to "Generalist Agents"-systems designed not for specific benchmarks but for open-ended utility across web, file, and coding domains.

### Magentic-One: A Generalist Multi-Agent System

**Paper Title: Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks (2024)**

**Paper Link:** [https://arxiv.org/abs/2411.04468]

#### Summary and Architectural Context

- Microsoft Research introduced Magentic-One, a high-performing open-source system designed to solve open-ended web and file-based tasks. 
- It moves beyond the rigid SOPs of MetaGPT to a dynamic orchestration model capable of handling the unpredictability of the real internet.

#### Architecture: Orchestrator and Ledgers

- The architecture is hierarchical, featuring a lead Orchestrator and specialized agents (WebSurfer, FileSurfer, Coder, ComputerTerminal). - The key innovation is the Orchestrator's dual-loop mechanism:
    - Outer Loop (Task Ledger): Maintains the high-level plan, gathered facts, and hypotheses. It breaks the user query into a strategic plan.
    - Inner Loop (Progress Ledger): Executes the specific steps of the plan. It assigns tasks to sub-agents, tracks their output, and monitors for "stalling" or repetitive loops.

#### Algorithmic Flow (Simplified Pseudocode):


```Python
while task_not_complete:
    Orchestrator checks Progress Ledger
    if progress_stalled:
        Update Task Ledger (Re-plan strategy)
    Select specialized_agent (e.g., WebSurfer)
    agent_output = specialized_agent.execute(action)
    Orchestrator updates Progress Ledger with agent_output
    Orchestrator reflects: "Did this solve the sub-step?"
```

- This "Ledger" concept effectively acts as a persistent, structured working memory, solving the "lost in the middle" phenomenon common in long-horizon tasks. 
- Magentic-One achieved competitive performance on GAIA, AssistantBench, and WebArena without benchmark-specific tuning.

### OpenDevin (OpenHands): The Open Platform for Generalist Agents

**Paper Title: OpenDevin: An Open Platform for AI Software Developers as Generalist Agents (2024)**

**Paper Link:** [https://arxiv.org/abs/2407.16741]

#### Summary

- OpenDevin (later renamed OpenHands) represents the community's response to proprietary agents like Devin. 
- It is an open platform designed to facilitate the development and evaluation of generalist agents that interact with the world via code, command line, and web browsing.

#### Key Contribution: Event Stream Architecture

- Unlike rigid agent frameworks, OpenDevin utilizes an Event Stream architecture. 
- All interactions-whether user messages, tool outputs, or agent thoughts-are treated as discrete events in a unified stream. This allows for:
    - Agnostic Agent Implementation: Researchers can swap out the agent "brain" (e.g., changing from a CodeAct agent to a Planner agent) while keeping the environment constant.
    - Sandboxed Execution: It integrates a secure runtime (based on Docker) that allows agents to execute destructive commands safely, a critical requirement for autonomous coding agents.
    - CodeAct: The platform popularized the CodeAct paradigm, where the agent writes executable Python code to perform all actions (including file manipulation and HTTP requests) rather than using distinct JSON-based tool calls. This unifies the action space and leverages the LLM's strong coding pre-training.
