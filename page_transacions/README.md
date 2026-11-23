The changes made in this version of the code are part of ongoing experiments conducted by the [Guara](https://github.com/douglasdcm/guara) team to improve the framework. These modifications were specifically selected because the code aligns well with the targets and goals of Guara, which aims to streamline automation processes, enhance maintainability, and improve clarity in its workflows.
Why This Code Was Selected for the Experiment:

    Fit with Guara’s Goals: The code was chosen because it focuses on automating flight data collection from the AENA website. This kind of task fits well within the scope of what the Guara framework is designed to handle—interacting with web data sources, managing transactions, and maintaining clear and efficient flows in automation tasks.

    Experimenting with Framework Improvements: The primary goal of these changes is to simplify and optimize the codebase, making it more modular, easier to extend, and simpler to maintain. The Guara team is experimenting with these adjustments to explore ways to make the framework more effective in automating workflows and providing better documentation for developers.

    Exploring Real-World Use Cases: By applying these modifications to a real-world use case—scraping flight data from AENA—the Guara team is experimenting with how best to structure the automation process, manage WebDriver interactions, and handle large data scraping tasks. The code has been adapted to better reflect the kinds of real-world scenarios that Guara is aiming to support in the future.

    Improvement of Error Handling and Status Management: Another area of focus is the improvement of error handling and status updates, which are crucial for any production-level automation. This experiment helps test and refine how Guara handles exceptions, monitors the progress of tasks, and logs detailed information about errors and successes. These features are critical for maintaining reliability and visibility during the execution of automated processes.


Key Improvements:

    Transactions:
        Individual transactions like InitializeBrowser, OpenAenaPage, ProcessAirportData, SaveFlightData, and CloseBrowser isolate distinct steps for reusability.

    Script Status Management:
        script_status is read, updated, and saved within a transaction to improve consistency.

    Data Processing:
        ProcessAirportData handles scraping logic for each airport independently.

    Orchestration:
        Application ensures sequential execution of transactions in the main flow.

    Modularity:
        Each transaction is responsible for a specific task, improving maintainability.

Conclusion:

The changes made in this version of the code are aligned with the Guara team’s broader objectives to refine and enhance the framework. By experimenting with these improvements, the team aims to develop more efficient, maintainable, and understandable automation scripts, ensuring that Guara continues to meet the needs of developers working on real-world automation tasks.