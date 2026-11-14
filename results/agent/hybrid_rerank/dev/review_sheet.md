# Review sheet: hybrid_rerank / dev

## d01 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is a single 1 or 0 stored inside a computer called?
- Expected: A binary digit, or bit.
- Queries: ['single binary digit 1 or 0 stored in computer called']
- Answer: A single 1 or 0 is called a binary digit, or bit [B:openstax-intro-cs:p205:c1].
- Citations: ['B:openstax-intro-cs:p205:c1']

## d02 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What term is used for the internal design of the processor?
- Expected: Microarchitecture.
- Queries: ['internal design of the processor term']
- Answer: The internal design of the processor (microprocessor) is called its microarchitecture. [B:openstax-intro-cs:p213:c0]
- Citations: ['B:openstax-intro-cs:p213:c0']

## d03 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: In IEEE 754 double precision, what value is subtracted from the exponent?
- Expected: 1023 (for single precision it is 127).
- Queries: ['IEEE 754 double precision exponent bias subtracted']
- Answer: For IEEE 754 double precision, 1023 is subtracted from the exponent (the bias), since the double precision format takes 64 bits [B:openstax-intro-cs:p220:c2]. The bias is 1023 in double precision, as stated in the denormalized-encoding discussion [B:openstax-intro-cs:p220:c3].
- Citations: ['B:openstax-intro-cs:p220:c2', 'B:openstax-intro-cs:p220:c3']

## d04 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: In the IEEE 754 format, what does it mean when the exponent is all 1s but the fraction is not zero?
- Expected: It is NaN (Not a Number) and raises an exception.
- Queries: ['IEEE 754 exponent all 1s fraction not zero NaN']
- Answer: When the exponent is all 1s and the fraction is non-zero, the value is NaN (Not a Number), and it raises an exception. This typically happens when a program has a bug, such as dividing by 0 or taking the square root of -1. [B:openstax-intro-cs:p220:c4]
- Citations: ['B:openstax-intro-cs:p220:c4']

## d05 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: When is the zero flag set to 1 in x86?
- Expected: When the previous instruction has generated 0 as a result.
- Queries: ['x86 zero flag set to 1']
- Answer: In x86, the zero flag is set to 1 when the previous instruction generated 0 as a result (for example, subtracting two registers and getting a result of 0). [B:openstax-intro-cs:p226:c4]
- Citations: ['B:openstax-intro-cs:p226:c4']

## d06 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is it called when the processor looks for data in the cache and the cache does not have it?
- Expected: A cache miss.
- Queries: ['processor looks for data in cache and cache does not have it']
- Answer: When the processor asks the cache for data and the cache does not have it, this is called a cache miss. [B:openstax-intro-cs:p232:c3]
- Citations: ['B:openstax-intro-cs:p232:c3']

## d07 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: How fast are sequential reads and writes on an SSD?
- Expected: Sequential read reaches 7000 MB/s and sequential write reaches 5000 MB/s.
- Queries: ['SSD sequential read and write speed']
- Answer: The text states that the sequential read from an SSD reaches 7000 MB/s and the sequential write reaches 5000 MB/s. Random access speeds are lower for both reads and writes [B:openstax-intro-cs:p234:c1].
- Citations: ['B:openstax-intro-cs:p234:c1']

## d08 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is the bootstrap code?
- Expected: A privileged system program; the first code executed when the OS starts.
- Queries: ['bootstrap code definition']
- Answer: The bootstrap code is a privileged system program that can run only in kernel mode; it is the first code executed when the OS starts, and the OS depends on it being loaded to work correctly [B:openstax-intro-cs:p262:c2].
- Citations: ['B:openstax-intro-cs:p262:c2']

## d09 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What was the first example of a layered operating system design and when was it designed?
- Expected: Dijkstra's THE system, designed in 1968.
- Queries: ['first example of layered operating system design']
- Answer: The first example of a layered approach was Dijkstra's THE system, designed in 1968. It had six layers (0 hardware up to 5 job manager) [B:openstax-intro-cs:p264:c0].
- Citations: ['B:openstax-intro-cs:p264:c0']

## d10 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is the name for moving the CPU from running one process to running another?
- Expected: A context switch.
- Queries: ['moving the CPU from running one process to another']
- Answer: The act of switching the CPU from one process to another is called a context switch [B:openstax-intro-cs:p273:c5].
- Citations: ['B:openstax-intro-cs:p273:c5']

## d11 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What problem occurs when memory blocks are too small to be given to processes and stay unused?
- Expected: Fragmentation.
- Queries: ['memory blocks too small to be allocated to processes remain unused']
- Answer: The problem is fragmentation. The source says that when memory blocks cannot be allocated to processes due to their small size and the blocks remain unused, this problem is called fragmentation [B:openstax-intro-cs:p279:c1]. (The passage also distinguishes internal fragmentation and external fragmentation.)
- Citations: ['B:openstax-intro-cs:p279:c1']

## d12 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What happens when the CPU requests a page that is not in main memory?
- Expected: A page fault occurs.
- Queries: ['page fault when CPU requests a page not in main memory']
- Answer: This is a page fault. The CPU transfers control from the program to the OS, which finds a free page frame in memory, loads the page from the backing store into main memory, and resumes execution of the thread; the CPU has special hardware to assist in resuming after the fault [B:openstax-intro-cs:p283:c0]. If all memory is in use, one page is swapped out to disk (page replacement) to make room [B:openstax-intro-cs:p283:c2].
- Citations: ['B:openstax-intro-cs:p283:c0', 'B:openstax-intro-cs:p283:c2']

## d13 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: Which encoding was approved in 1963 and later revised several times, and in which years was it revised?
- Expected: ASCII; approved in 1963 and revised in 1965, 1967, 1968, 1977 and 1986.
- Queries: ['encoding approved 1963 revised several times']
- Answer: The encoding is ASCII (American Standard Code for Information Interchange), approved in 1963 and then revised in 1965, 1967, 1968, 1977, and 1986. [B:openstax-intro-cs:p218:c2]
- Citations: ['B:openstax-intro-cs:p218:c2']

## d14 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What technique does the operating system use to keep programs from overwriting each other's data, and what is it called?
- Expected: Virtual memory: the OS isolates programs so they do not overwrite each other's data or corrupt each other's files.
- Queries: ["operating system memory protection keeps programs from overwriting each other's data"]
- Answer: The OS isolates programs from each other so they do not overwrite each other's data or corrupt each other's files using a technique called virtual memory [B:openstax-intro-cs:p214:c1].
- Citations: ['B:openstax-intro-cs:p214:c1']

## d15 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What does scheduling mean?
- Expected: Choosing which process to run next (removing the running process from the CPU and selecting another one according to a strategy).
- Queries: ['what does scheduling mean in an operating system']
- Answer: Scheduling is choosing which process to run next: it is the activity of removing the running process from the CPU and selecting another process based on a particular strategy [B:openstax-intro-cs:p272:c3]. More generally, it is determining which process in the ready state should move to the running state when more resources are requested than can be granted immediately, and the order in which those requests are serviced [B:openstax-intro-cs:p274:c0].
- Citations: ['B:openstax-intro-cs:p272:c3', 'B:openstax-intro-cs:p274:c0']

## d16 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: According to Moore's law, how often would the number of devices inside the processor double?
- Expected: Every 18 months (Gordon Moore's 1965 prediction).
- Queries: ["Moore's law number of devices inside processor double"]
- Answer: According to Moore's law, the number of devices inside the processor would double every 18 months [B:openstax-intro-cs:p236:c4].
- Citations: ['B:openstax-intro-cs:p236:c4']

## d17 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is Intel's name for simultaneous multithreading?
- Expected: Hyperthreading technology.
- Queries: ['Intel name for simultaneous multithreading']
- Answer: Intel calls simultaneous multithreading (SMT) "hyperthreading technology." [B:openstax-intro-cs:p238:c1]
- Citations: ['B:openstax-intro-cs:p238:c1']

## d18 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What does a journaling file system do?
- Expected: It records the changes in a separate log file, sometimes called a journal file.
- Queries: ['journaling file system']
- Answer: A journaling file system uses write-ahead logging: it records the changes to information in a separate log file (the journal), and these changes are recorded before any new change or update is made to the system [B:openstax-intro-cs:p292:c1].
- Citations: ['B:openstax-intro-cs:p292:c1']

## d19 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: How does the storage access latency of disks compare with that of flash memory?
- Expected: About 10 ms for disks versus about 100 µs for flash memory.
- Queries: ['storage access latency disk versus flash memory']
- Answer: Disks have a storage access latency of around 10 ms, while flash memory's is around 100 µs, so flash is roughly 100 times lower in latency than disk. [B:openstax-intro-cs:p293:c2]
- Citations: ['B:openstax-intro-cs:p293:c2']

## d20 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: Why are SSDs faster and more durable than hard disk drives?
- Expected: SSDs have no moving/mechanical parts (unlike HDDs with rotating disks and read/write heads), which increases durability and makes reads and writes much faster.
- Queries: ['why are SSDs faster and more durable than hard disk drives']
- Answer: SSDs have no moving parts, unlike HDDs with rotating disks and read/write heads, which increases durability and lets data be read and written much faster. Flash memory also allows random access, so scattered data is read quicker than with HDDs, which must physically move the read/write head; the lack of a head to position also lowers latency [B:openstax-intro-cs:p288:c3][B:openstax-intro-cs:p288:c4].
- Citations: ['B:openstax-intro-cs:p288:c3', 'B:openstax-intro-cs:p288:c4']

## d21 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is a thread?
- Expected: A path of execution within a process (a basic unit of execution); a process may contain multiple threads that share its resources.
- Queries: ['what is a thread']
- Answer: A thread is the OS's unit of concurrency and the abstraction of a virtual CPU core: a basic unit of execution that runs a set of instructions in a specific order. It is a lightweight process that shares OS resources (such as memory and I/O) with other threads in the same process, and threads are essentially paths of execution within a process [B:openstax-intro-cs:p271:c1]. Threads are created by the OS kernel, each has its own register stack, and all threads in a process share the same memory space [B:openstax-intro-cs:p271:c1].
- Citations: ['B:openstax-intro-cs:p271:c1']

## d22 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What do we call the group of wires that links the CPU, the memory and the graphics card so they can exchange data?
- Expected: A bus (a collection of wires that transfers data between the components).
- Queries: ['bus wires link CPU memory graphics card exchange data']
- Answer: The group of wires is called a bus. It connects the CPU, memory and graphics card and transfers data between these components [B:openstax-intro-cs:p207:c0].
- Citations: ['B:openstax-intro-cs:p207:c0']

## d23 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: In one's complement representation, how can you tell that a binary number is negative?
- Expected: If the most significant bit is 1, the number is negative (it is stored in one's complement form; taking the one's complement again gives the original magnitude).
- Queries: ["one's complement representation negative number leftmost bit"]
- Answer: In one's complement, you check the most significant (leftmost) bit: if it is 1, the number is negative and is stored in its one's complement form (you must take the one's complement to recover the original magnitude). If it is 0, the number is positive. [B:openstax-intro-cs:p216:c4]
- Citations: ['B:openstax-intro-cs:p216:c4']

## d24 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: In operating system design, which concept decides what should be done and which concept carries out how it is done?
- Expected: A policy decides what needs to be done; a mechanism is the activity that enforces the policy (how to do it).
- Queries: ['operating system policy versus mechanism distinction']
- Answer: A policy decides what needs to be done (choosing which activities to perform), and a mechanism carries out how it is done (the activity that enforces the policies) [B:openstax-intro-cs:p253:c0].
- Citations: ['B:openstax-intro-cs:p253:c0']

## d25 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: Which piece of software lets one physical server host several guest operating systems by creating and managing virtual machines?
- Expected: A hypervisor (virtual machine monitor, VMM).
- Queries: ['software that hosts multiple guest operating systems by creating and managing virtual machines']
- Answer: A hypervisor (also called a virtual machine monitor, or VMM) is the software layer placed between a server's hardware and its operating systems; it creates and manages the virtual machines that run the guest operating systems [B:openstax-intro-cs:p253:c2].
- Citations: ['B:openstax-intro-cs:p253:c2']

## d26 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: On a UNIX-like system, where is the mapping from a file's name to its inode kept?
- Expected: In directories, which are special files listing file names and their corresponding inodes (the inode itself does not contain the name).
- Queries: ['UNIX file name to inode mapping directory']
- Answer: On a UNIX-like system, the name-to-inode mapping is stored in directories. Directories are special files that list file names and their corresponding inodes [B:openstax-intro-cs:p285:c3]; each directory holds <name, address> pairs [B:openstax-intro-cs:p284:c3].
- Citations: ['B:openstax-intro-cs:p285:c3', 'B:openstax-intro-cs:p284:c3']

## ud01 (UNANSWERABLE) | status=abstain | searches=3 | context_hit=None | cited_gold_chunk=None
- Q: What is the maximum file size supported by the FAT32 file system?
- Expected: The corpus only describes FAT as a table mapping file names to clusters (p285); it never mentions FAT32 or any file size limit.
- Queries: ['FAT32 maximum file size', 'FAT32 file system limit 4 GB file size', 'FAT32 supports files up to']
- Answer: The passages do not state the maximum file size supported by FAT32. They only describe FAT as a table-based file location method and NTFS as using a Master File Table [B:openstax-intro-cs:p285:c4], so the specific limit is not given in the retrieved material.
- Citations: []

## ud02 (UNANSWERABLE) | status=abstain | searches=3 | context_hit=None | cited_gold_chunk=None
- Q: How many transistors does Intel's Core i9 processor contain?
- Expected: The corpus only says generally that a single processor contains billions of transistors (p213); no specific Intel Core i9 figure exists.
- Queries: ['Intel Core i9 processor number of transistors', 'Core i9 transistors million figure x86 processor generations table', 'Intel Core i9 transistor count']
- Answer: The passages do not state how many transistors Intel's Core i9 processor contains. They only say that Intel's x86 generations saw a "tremendous increase in transistors" without giving any Core i9 figure.
- Citations: []

## ud03 (UNANSWERABLE) | status=abstain | searches=3 | context_hit=None | cited_gold_chunk=None
- Q: Which page replacement algorithm does Windows 11 use?
- Expected: Page replacement is defined generically (p283) but no algorithm per OS and no Windows 11 are mentioned.
- Queries: ['Windows 11 page replacement algorithm', 'Windows operating system page replacement policy clock least recently used', 'Windows 11 operating system memory management']
- Answer: The retrieved passages do not say which page replacement algorithm Windows 11 uses. They only describe page replacement in general (swapping a page to disk when memory is full) and thrashing [B:openstax-intro-cs:p283:c2].
- Citations: []
