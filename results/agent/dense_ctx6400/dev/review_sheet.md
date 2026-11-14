# Review sheet: dense_ctx6400 / dev

## d01 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is a single 1 or 0 stored inside a computer called?
- Expected: A binary digit, or bit.
- Queries: ['single 1 or 0 stored in a computer called a bit']
- Answer: A 1 or a 0 stored inside a computer is called a binary digit, or bit. [B:openstax-intro-cs:p205:c1]
- Citations: ['B:openstax-intro-cs:p205:c1']

## d02 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What term is used for the internal design of the processor?
- Expected: Microarchitecture.
- Queries: ['internal design of the processor term']
- Answer: The internal design of the processor is called its microarchitecture: "The architecture (i.e., design) of the microprocessor (i.e., the processor) is called microarchitecture" [B:openstax-intro-cs:p213:c0].
- Citations: ['B:openstax-intro-cs:p213:c0']

## d03 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: In IEEE 754 double precision, what value is subtracted from the exponent?
- Expected: 1023 (for single precision it is 127).
- Queries: ['IEEE 754 double precision exponent bias subtracted']
- Answer: For IEEE 754 double precision, 1023 is subtracted from the exponent (the bias), since double precision takes 64 bits [B:openstax-intro-cs:p220:c2]. This bias is 1023 for double precision, versus 127 for single precision [B:openstax-intro-cs:p220:c3].
- Citations: ['B:openstax-intro-cs:p220:c2', 'B:openstax-intro-cs:p220:c3']

## d04 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: In the IEEE 754 format, what does it mean when the exponent is all 1s but the fraction is not zero?
- Expected: It is NaN (Not a Number) and raises an exception.
- Queries: ['IEEE 754 exponent all 1s fraction not zero']
- Answer: When the exponent is all 1s and the fraction is non-zero, the value is called NaN (Not a Number) and it raises an exception. This typically happens when there is a bug in the program, such as dividing by 0 or taking the square root of -1 [B:openstax-intro-cs:p220:c4].
- Citations: ['B:openstax-intro-cs:p220:c4']

## d05 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: When is the zero flag set to 1 in x86?
- Expected: When the previous instruction has generated 0 as a result.
- Queries: ['zero flag set to 1 x86']
- Answer: In x86, the zero flag is set to 1 when the previous instruction generated 0 as a result, for example when subtracting two registers gives a result of 0 [B:openstax-intro-cs:p226:c4].
- Citations: ['B:openstax-intro-cs:p226:c4']

## d06 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is it called when the processor looks for data in the cache and the cache does not have it?
- Expected: A cache miss.
- Queries: ['cache miss processor looks for data in cache and it is not there']
- Answer: It is called a cache miss. When the processor asks the cache for data it needs and the cache does not have it, the cache must fetch the data from memory [B:openstax-intro-cs:p232:c3].
- Citations: ['B:openstax-intro-cs:p232:c3']

## d07 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: How fast are sequential reads and writes on an SSD?
- Expected: Sequential read reaches 7000 MB/s and sequential write reaches 5000 MB/s.
- Queries: ['SSD sequential read and write speed']
- Answer: According to the text, sequential reads from an SSD reach 7000 MB/s and sequential writes reach 5000 MB/s. Random access has lower speeds for both reads and writes. [B:openstax-intro-cs:p234:c1]
- Citations: ['B:openstax-intro-cs:p234:c1']

## d08 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is the bootstrap code?
- Expected: A privileged system program; the first code executed when the OS starts.
- Queries: ['bootstrap code definition']
- Answer: The bootstrap code is a privileged system program that can run only in kernel mode; it is the first code executed when the OS starts, and the OS depends on it being loaded and working correctly [B:openstax-intro-cs:p262:c2].
- Citations: ['B:openstax-intro-cs:p262:c2']

## d09 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What was the first example of a layered operating system design and when was it designed?
- Expected: Dijkstra's THE system, designed in 1968.
- Queries: ['first example of layered operating system design']
- Answer: The first example of a layered approach was Dijkstra's THE system, designed in 1968. It had six layers (0 to 5), from hardware at the bottom up to the job manager that executes users' programs. [B:openstax-intro-cs:p264:c0]
- Citations: ['B:openstax-intro-cs:p264:c0']

## d10 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is the name for moving the CPU from running one process to running another?
- Expected: A context switch.
- Queries: ['moving CPU from running one process to another']
- Answer: The act of switching the CPU from one process to another is called a context switch [B:openstax-intro-cs:p273:c5].
- Citations: ['B:openstax-intro-cs:p273:c5']

## d11 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What problem occurs when memory blocks are too small to be given to processes and stay unused?
- Expected: Fragmentation.
- Queries: ['memory blocks too small to be allocated to processes remain unused']
- Answer: The problem is fragmentation: when memory blocks are too small to be allocated to processes and remain unused, this is called fragmentation [B:openstax-intro-cs:p279:c1]. The passage names two types, internal fragmentation (allocated block exceeds process size, leaving part unused) and external fragmentation (enough total space exists but is not contiguous) [B:openstax-intro-cs:p279:c1].
- Citations: ['B:openstax-intro-cs:p279:c1']

## d12 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What happens when the CPU requests a page that is not in main memory?
- Expected: A page fault occurs.
- Queries: ['page fault when CPU requests a page not in main memory']
- Answer: This is a page fault. The CPU transfers control from the program to the OS, which finds a free page frame in memory, loads the page from the backing store into main memory, and resumes execution of the thread; the CPU has special hardware to help resume after a page fault [B:openstax-intro-cs:p283:c0]. If all memory is in use, one page is first replaced (swapped to disk) to make room [B:openstax-intro-cs:p283:c2].
- Citations: ['B:openstax-intro-cs:p283:c0', 'B:openstax-intro-cs:p283:c2']

## d13 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: Which encoding was approved in 1963 and later revised several times, and in which years was it revised?
- Expected: ASCII; approved in 1963 and revised in 1965, 1967, 1968, 1977 and 1986.
- Queries: ['encoding approved in 1963 revised several times']
- Answer: The encoding is ASCII (American Standard Code for Information Interchange), approved in 1963 and later revised in 1965, 1967, 1968, 1977, and 1986 [B:openstax-intro-cs:p218:c2].
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
- Queries: ['what is scheduling in an operating system']
- Answer: Scheduling is the act of determining which process in the ready state should be moved to the running state when more resources are requested than can be granted immediately, and in what order such requests should be serviced [B:openstax-intro-cs:p274:c0]. It is also described as choosing which process to run next, i.e., handling the removal of the running process from the CPU and selecting another based on a particular strategy [B:openstax-intro-cs:p272:c3].
- Citations: ['B:openstax-intro-cs:p274:c0', 'B:openstax-intro-cs:p272:c3']

## d16 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: According to Moore's law, how often would the number of devices inside the processor double?
- Expected: Every 18 months (Gordon Moore's 1965 prediction).
- Queries: ["Moore's law number of devices in processor doubles"]
- Answer: According to Moore's law, the number of devices inside the processor would double every 18 months [B:openstax-intro-cs:p236:c4].
- Citations: ['B:openstax-intro-cs:p236:c4']

## d17 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is Intel's name for simultaneous multithreading?
- Expected: Hyperthreading technology.
- Queries: ['Intel name for simultaneous multithreading']
- Answer: Intel calls simultaneous multithreading (SMT) "hyperthreading technology" [B:openstax-intro-cs:p238:c1].
- Citations: ['B:openstax-intro-cs:p238:c1']

## d18 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What does a journaling file system do?
- Expected: It records the changes in a separate log file, sometimes called a journal file.
- Queries: ['journaling file system what does it do']
- Answer: A journaling file system performs write-ahead logging: it records the changes to information in a separate log file, called a journal, before any new change or update is made to the system [B:openstax-intro-cs:p292:c1].
- Citations: ['B:openstax-intro-cs:p292:c1']

## d19 (answerable) | status=answered | searches=2 | context_hit=False | cited_gold_chunk=False
- Q: How does the storage access latency of disks compare with that of flash memory?
- Expected: About 10 ms for disks versus about 100 µs for flash memory.
- Queries: ['storage access latency disk versus flash memory', 'hard disk drive access time milliseconds latency rotational seek']
- Answer: Disks (HDDs) are very slow compared with flash memory: HDDs are "several orders of magnitude slower than the DRAM memory" because of mechanical movement, whereas flash-based SSDs have no moving parts and can access data much faster, with random access that avoids moving the read/write head. The sources do not give specific latency numbers for either device, so the comparison is qualitative. [B:openstax-intro-cs:p233:c2] [B:openstax-intro-cs:p288:c3]
- Citations: ['B:openstax-intro-cs:p233:c2', 'B:openstax-intro-cs:p288:c3']

## d20 (answerable) | status=answered | searches=2 | context_hit=True | cited_gold_chunk=True
- Q: Why are SSDs faster and more durable than hard disk drives?
- Expected: SSDs have no moving/mechanical parts (unlike HDDs with rotating disks and read/write heads), which increases durability and makes reads and writes much faster.
- Queries: ['why are SSDs faster and more durable than hard disk drives', 'solid state drive no moving parts compared to hard disk drive']
- Answer: SSDs have no moving parts, unlike HDDs, which use rotating disks and read/write heads. Because there is no mechanical part to wear out or fail, SSDs are more durable and reliable and can better withstand drops or impacts [B:openstax-intro-cs:p288:c3][B:openstax-intro-cs:p288:c4]. Their speed comes from flash memory's random access, which avoids the time HDDs need to physically move the read/write head, and from lower latency and faster read/write operations [B:openstax-intro-cs:p288:c3][B:openstax-intro-cs:p288:c4].
- Citations: ['B:openstax-intro-cs:p288:c3', 'B:openstax-intro-cs:p288:c4']

## d21 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What is a thread?
- Expected: A path of execution within a process (a basic unit of execution); a process may contain multiple threads that share its resources.
- Queries: ['what is a thread']
- Answer: A thread is the OS's unit of concurrency and the abstraction of a virtual CPU core: a basic unit of execution that runs a set of instructions in a specific order. It is a lightweight process that shares OS resources (such as memory and I/O) with other threads in the same process, and each thread has its own register stack [B:openstax-intro-cs:p271:c1]. A thread is a smaller or lightweight portion of a process that is managed independently [B:openstax-intro-cs:p258:c0].
- Citations: ['B:openstax-intro-cs:p271:c1', 'B:openstax-intro-cs:p258:c0']

## d22 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: What do we call the group of wires that links the CPU, the memory and the graphics card so they can exchange data?
- Expected: A bus (a collection of wires that transfers data between the components).
- Queries: ['group of wires linking CPU, memory and graphics card to exchange data']
- Answer: The group of wires is called a bus. It is a collection of wires that connects the CPU, memory and graphics card and transfers data between them [B:openstax-intro-cs:p207:c0].
- Citations: ['B:openstax-intro-cs:p207:c0']

## d23 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: In one's complement representation, how can you tell that a binary number is negative?
- Expected: If the most significant bit is 1, the number is negative (it is stored in one's complement form; taking the one's complement again gives the original magnitude).
- Queries: ["one's complement representation negative number leading bit"]
- Answer: In one's complement, check the most significant bit: if it is 1, the number is negative and is stored in its one's complement form (you must take the one's complement again to find its original value). If it is 0, the number is positive and is read as unsigned. [B:openstax-intro-cs:p216:c4]
- Citations: ['B:openstax-intro-cs:p216:c4']

## d24 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: In operating system design, which concept decides what should be done and which concept carries out how it is done?
- Expected: A policy decides what needs to be done; a mechanism is the activity that enforces the policy (how to do it).
- Queries: ['operating system policy versus mechanism separation what should be done versus how it is done']
- Answer: A policy decides what needs to be done (which activities to perform), and a mechanism is the activity that enforces the policy and carries out how to do it [B:openstax-intro-cs:p253:c0].
- Citations: ['B:openstax-intro-cs:p253:c0']

## d25 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: Which piece of software lets one physical server host several guest operating systems by creating and managing virtual machines?
- Expected: A hypervisor (virtual machine monitor, VMM).
- Queries: ['software that hosts multiple guest operating systems by creating and managing virtual machines']
- Answer: A hypervisor (also called a virtual machine monitor, or VMM) is the software layer placed between a server's hardware and the operating systems that run on it; it creates and manages virtual machines [B:openstax-intro-cs:p253:c2]. It allocates physical resources to each VM and keeps them isolated from one another [B:openstax-intro-cs:p293:c5].
- Citations: ['B:openstax-intro-cs:p253:c2', 'B:openstax-intro-cs:p293:c5']

## d26 (answerable) | status=answered | searches=1 | context_hit=True | cited_gold_chunk=True
- Q: On a UNIX-like system, where is the mapping from a file's name to its inode kept?
- Expected: In directories, which are special files listing file names and their corresponding inodes (the inode itself does not contain the name).
- Queries: ['UNIX file name to inode mapping directory']
- Answer: On a UNIX-like system, the name-to-inode mapping is stored in directories, which are special files that list file names and their corresponding inodes [B:openstax-intro-cs:p285:c3]. Directories store <name, address> pairs on disk like regular files [B:openstax-intro-cs:p284:c3].
- Citations: ['B:openstax-intro-cs:p285:c3', 'B:openstax-intro-cs:p284:c3']

## ud01 (UNANSWERABLE) | status=abstain | searches=3 | context_hit=None | cited_gold_chunk=None
- Q: What is the maximum file size supported by the FAT32 file system?
- Expected: The corpus only describes FAT as a table mapping file names to clusters (p285); it never mentions FAT32 or any file size limit.
- Queries: ['FAT32 maximum file size', 'FAT32 file system 4 GB file size limit', 'FAT32 limitations maximum size of a single file']
- Answer: The passages do not state the maximum file size supported by FAT32. They only describe FAT generally as a table mapping files to disk clusters [B:openstax-intro-cs:p285:c4], so the question cannot be answered from this collection.
- Citations: []

## ud02 (UNANSWERABLE) | status=abstain | searches=3 | context_hit=None | cited_gold_chunk=None
- Q: How many transistors does Intel's Core i9 processor contain?
- Expected: The corpus only says generally that a single processor contains billions of transistors (p213); no specific Intel Core i9 figure exists.
- Queries: ['Intel Core i9 processor number of transistors', 'Core i9 transistors figure processor generation table', 'transistor count Intel processors 4004 8086 Pentium Core i7 i9']
- Answer: The retrieved passages do not state how many transistors Intel's Core i9 processor contains. They only say that x86 generations show a "tremendous increase in transistors" and that Moore's law predicted device counts would double every 18 months, without giving a Core i9 figure.
- Citations: []

## ud03 (UNANSWERABLE) | status=abstain | searches=3 | context_hit=None | cited_gold_chunk=None
- Q: Which page replacement algorithm does Windows 11 use?
- Expected: Page replacement is defined generically (p283) but no algorithm per OS and no Windows 11 are mentioned.
- Queries: ['Windows 11 page replacement algorithm', 'Windows operating system page replacement policy clock least recently used', 'page replacement algorithms FIFO LRU clock second chance']
- Answer: The passages do not say which page replacement algorithm Windows 11 uses. They only describe page replacement and paging generally, without mentioning Windows 11 or any specific algorithm it uses.
- Citations: []
