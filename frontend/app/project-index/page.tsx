"use client";

import React from "react";

export default function ProjectIndexPage() {
    const tableData = [
        {
            title: "1. Introduction",
            subtopics: [
                { name: "1.1 Project Description (2-4 Pages)", pages: "00" },
                { name: "1.2 Company Profile (1-2-3 Pages)", pages: "00" },
            ],
            pages: "00",
            isMain: true,
        },
        {
            title: "2. Literature Survey",
            subtopics: [
                { name: "2.1 Existing And Proposed System (2-3 Pages)", pages: "00" },
                { name: "2.2 Feasibility Study (2-3 Pages)", pages: "00" },
                { name: "2.3 Tools And Technologies Used (2-4 Pages)", pages: "00" },
                { name: "2.4 Hardware And Software Requirements (1 Page)", pages: "00" },
            ],
            pages: "00",
            isMain: true,
        },
        {
            title: "3. Software Requirements Specification",
            subtopics: [
                { name: "3.1 Users (2-3 Pages)", pages: "00" },
                { name: "3.2 Functional Requirements (2-3 Pages)", pages: "00" },
                { name: "3.3 Non-functional Requirements (2-3 Pages)", pages: "00" },
            ],
            pages: "00",
            isMain: true,
        },
        {
            title: "4. System Design (high Level or Architectural Design)",
            subtopics: [
                { name: "4.1 System Perspective (1-2 Pages)", pages: "00" },
                { name: "4.2 Context Diagram (1-2 Pages)", pages: "00" },
            ],
            pages: "00",
            isMain: true,
        },
        {
            title: "5. Detailed Design (various Design Diagrams According to Project)",
            subtopics: [
                { name: "5.1 Use Case Diagram (4-6 Pages)", pages: "00" },
                { name: "5.2 Sequence Diagrams (4-6 Pages)", pages: "00" },
                { name: "5.3 Collaboration Diagrams (3-5 Pages)", pages: "00" },
                { name: "5.4 Activity Diagram (4-6 Pages)", pages: "00" },
                { name: "5.5 Database Design (ER and/or Conceptual Schema) (3-4 Pages)", pages: "00" },
            ],
            pages: "00",
            isMain: true,
        },
        {
            title: "6. Implementation (no Full Code, Code Snippet May Be Included)",
            subtopics: [
                { name: "6.1 Screen Shots (15-20 Pages)", pages: "00" },
            ],
            pages: "00",
            isMain: true,
        },
        {
            title: "7. Software Testing (test Cases Etc.) (6-8 Pages)",
            subtopics: [],
            pages: "00",
            isMain: true,
        },
        {
            title: "8. Conclusion (1 Page)",
            subtopics: [],
            pages: "00",
            isMain: true,
        },
        {
            title: "9. Future Enhancements (1 Page)",
            subtopics: [],
            pages: "00",
            isMain: true,
        },
        {
            title: "Appendix A",
            subtopics: [{ name: "Bibliography (1 Page)", pages: "00" }],
            pages: "",
            isMain: true,
            customLayout: true,
        },
        {
            title: "Appendix B",
            subtopics: [{ name: "User Manual (2-10 Pages)", pages: "00" }],
            pages: "",
            isMain: true,
            customLayout: true,
        },
    ];

    return (
        <div className="min-h-screen bg-white p-8 md:p-12 text-black font-sans">
            <div className="max-w-5xl mx-auto">
                <h1 className="text-center text-2xl md:text-3xl font-bold text-pink-600 mb-8 uppercase tracking-wide">
                    Contents (for Application Oriented Projects)
                </h1>

                <div className="border border-black">
                    {/* Header */}
                    <div className="grid grid-cols-12 bg-gray-100 border-b border-black font-bold text-sm md:text-base">
                        <div className="col-span-4 p-3 border-r border-black text-center uppercase text-pink-600">Title</div>
                        <div className="col-span-6 p-3 border-r border-black text-center uppercase text-pink-600">Subtopics</div>
                        <div className="col-span-2 p-3 text-center uppercase text-pink-600">Pages</div>
                    </div>

                    {/* Body */}
                    {tableData.map((section, index) => (
                        <React.Fragment key={index}>
                            {/* Main Section Row */}
                            <div className="grid grid-cols-12 border-b border-black last:border-b-0">
                                {/* Title Column */}
                                <div className="col-span-4 p-3 border-r border-black font-bold text-pink-600">
                                    {section.title}
                                </div>

                                {/* Subtopics Column */}
                                <div className="col-span-6 p-0 border-r border-black">
                                    {section.subtopics.length > 0 ? (
                                        section.subtopics.map((sub, idx) => (
                                            <div
                                                key={idx}
                                                className={`p-2 pl-4 ${idx !== section.subtopics.length - 1 ? "border-b border-gray-300" : ""
                                                    }`}
                                            >
                                                {section.customLayout ? (
                                                    <div className="flex justify-between">
                                                        <span>{sub.name.split("   ")[0]}</span> {/* Handle potential spacing manual formatting if needed, but flex justify-between works well */}
                                                    </div>
                                                ) : (
                                                    sub.name
                                                )}
                                            </div>
                                        ))
                                    ) : (
                                        <div className="p-3 text-gray-500 italic"></div>
                                    )}
                                </div>

                                {/* Pages Column */}
                                <div className="col-span-2 p-0 text-center">
                                    {/* For the main section page number */}
                                    {section.subtopics.length === 0 && (
                                        <div className="p-3 font-bold h-full flex items-center justify-center">{section.pages}</div>
                                    )}

                                    {/* For subtopic page numbers */}
                                    {section.subtopics.length > 0 && section.subtopics.map((sub, idx) => (
                                        <div
                                            key={idx}
                                            className={`p-2 ${idx !== section.subtopics.length - 1 ? "border-b border-gray-300" : ""
                                                } h-full flex items-center justify-center`}
                                        >
                                            {sub.pages}
                                        </div>
                                    ))}

                                    {/* If it's an appendix with custom layout where page number is aligned with subtopic */}
                                </div>
                            </div>
                        </React.Fragment>
                    ))}
                </div>

                {/* Special handling for Appendix if needed to match exact visual style of right-aligned sub-items with their own page numbers, 
            but the table structure above should cover it cleanly enough. 
            Refining the Appendix display to match the "Bibliography (1 Page) 00" format in the image where it looks like part of the line.
            Visual fix: The image shows Appendix A on left, Bibliography on right. 
            My table structure puts Bibliography in the middle column. 
            Let's keep it consistent: Title | Subtopic | Page
            Appendix A | Bibliography | 00
            This works.
        */}

            </div>
        </div>
    );
}
