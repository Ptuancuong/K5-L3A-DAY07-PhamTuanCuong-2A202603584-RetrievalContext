# Review sheet: chosen / test

## t01 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What piece of software takes a program written in a high-level language and turns it into assembly language?
- Expected: A compiler.
- Queries: ['What piece of software takes a program written in a high-level language and turns it into assembly language?']
- Answer: A compiler. It is a piece of software that takes a program written in a given high-level language and generates another program, written in assembly language, that does the same task [B:openstax-intro-cs:p210:c4].
- Citations: ['B:openstax-intro-cs:p210:c4']

## t02 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: Between the CPU and memory, which bus is single directional and which is bidirectional, and why is the latter bidirectional?
- Expected: The address bus is single directional (the CPU always provides the address); the data bus is bidirectional because data can be sent to memory or fetched from memory.
- Queries: ['Between the CPU and memory, which bus is single directional and which is bidirectional, and why is the latter bidirectional?']
- Answer: The address bus is single directional and the data bus is bidirectional. The CPU must always provide an address (to read or write memory), so the address bus runs one way. The data bus is bidirectional because data can be sent from the CPU to memory (for writes) or retrieved from memory to the CPU (for reads) [B:openstax-intro-cs:p223:c2].
- Citations: ['B:openstax-intro-cs:p223:c2']

## t03 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What five properties should an ideal memory system have?
- Expected: Fast, dense, persistent, large in capacity, and inexpensive.
- Queries: ['What five properties should an ideal memory system have?']
- Answer: An ideal memory system must be fast, dense, persistent, large in capacity, and inexpensive [B:openstax-intro-cs:p229:c0].
- Citations: ['B:openstax-intro-cs:p229:c0']

## t04 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: In UNIX, which two operations split process creation into two steps?
- Expected: fork (creates a complete copy of the process) and exec (brings the executable file into memory to start execution).
- Queries: ['In UNIX, which two operations split process creation into two steps?']
- Answer: In UNIX, process creation is split into two steps using the fork and exec functionalities. Fork creates a complete copy of the process (to set up privileges), and exec brings the executable file into memory to start execution. [B:openstax-intro-cs:p258:c2]
- Citations: ['B:openstax-intro-cs:p258:c2']

## t05 (answerable) | status=answered | searches=2 | context_hit=True | cited_gold_chunk=True
- Q: At a minimum, what does a process consist of?
- Expected: An address space, a CPU state, and a set of OS resources.
- Queries: ['At a minimum, what does a process consist of?', 'process consists of program counter, registers, and memory, minimum components of a process']
- Answer: At a minimum, a process consists of an address space, a CPU state, and a set of OS resources [B:openstax-intro-cs:p268:c1]. The address space holds the running program's instruction code and data, and the CPU state consists of the program counter, the stack pointer, and general-purpose registers [B:openstax-intro-cs:p268:c1].
- Citations: ['B:openstax-intro-cs:p268:c1']

## t06 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What hardware cache speeds up translating virtual addresses into physical addresses?
- Expected: The translation lookaside buffer (TLB), a memory cache that stores recent virtual-to-physical translations.
- Queries: ['What hardware cache speeds up translating virtual addresses into physical addresses?']
- Answer: The translation lookaside buffer (TLB), a hardware memory cache that stores recent virtual-to-physical address translations, speeds up address translation [B:openstax-intro-cs:p281:c3].
- Citations: ['B:openstax-intro-cs:p281:c3']

## t07 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: After a website has set the two-factor authentication cookie, when is two-factor authentication required again?
- Expected: Whenever the user logs in from a different browser or a different machine.
- Queries: ['After a website has set the two-factor authentication cookie, when is two-factor authentication required again?']
- Answer: Two-factor authentication is used again whenever a user needs to log in from a different browser or different machine. Until then, the cookie lets the browser log in with the password as long as the cookie persists [B:openstax-intro-cs:p290:c1][B:openstax-intro-cs:p290:c2].
- Citations: ['B:openstax-intro-cs:p290:c1', 'B:openstax-intro-cs:p290:c2']

## t08 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: Which file system operation resets a file's length to zero and releases its allocated space?
- Expected: Truncate.
- Queries: ["Which file system operation resets a file's length to zero and releases its allocated space?"]
- Answer: The Truncate operation: it resets the file length to zero and releases the allocated space for the file [B:openstax-intro-cs:p286:c1].
- Citations: ['B:openstax-intro-cs:p286:c1']

## ut01 (UNANSWERABLE) | status=abstain | searches=3 | context_hit=None | cited_gold_chunk=None
- Q: What is the default time quantum used by the Linux Completely Fair Scheduler?
- Expected: Round-robin time slices are explained with a toy example (p274, p278: 2 ms slice), but the Linux Completely Fair Scheduler and its defaults are never mentioned.
- Queries: ['What is the default time quantum used by the Linux Completely Fair Scheduler?', 'Completely Fair Scheduler Linux time slice default value', 'Linux CFS scheduler quantum milliseconds']
- Answer: The passages do not state the default time quantum used by the Linux Completely Fair Scheduler. They only describe round-robin and time-slicing generally, with no Linux CFS default value given.
- Citations: []

## ut02 (UNANSWERABLE) | status=abstain | searches=3 | context_hit=None | cited_gold_chunk=None
- Q: How much L3 cache does Apple's M2 chip have?
- Expected: L3 cache appears only in the generic cache-level explanation (p235); Apple is mentioned only for macOS; no M2 chip.
- Queries: ["How much L3 cache does Apple's M2 chip have?", 'Apple M2 chip cache size', 'M2 chip L3 cache megabytes']
- Answer: The passages do not say how much L3 cache Apple's M2 chip has. They only state that most processors now have up to three cache levels and that the processor's cache size is often unknown to the user [B:openstax-intro-cs:p234:c3][B:openstax-intro-cs:p232:c2].
- Citations: []

## ut03 (UNANSWERABLE) | status=abstain | searches=3 | context_hit=None | cited_gold_chunk=None
- Q: In what year did Microsoft first introduce the NTFS file system?
- Expected: NTFS is described (Master File Table, p285; journaling, p292) but its introduction year is not given.
- Queries: ['In what year did Microsoft first introduce the NTFS file system?', 'NTFS introduced Windows NT year', 'New Technology File System Microsoft history release date']
- Answer: The passages do not state the year Microsoft first introduced NTFS. They only describe how NTFS locates files using the Master File Table [B:openstax-intro-cs:p285:c4]; the year is not given.
- Citations: []
